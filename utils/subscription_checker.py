from datetime import datetime, timedelta
from sqlalchemy import select, update
import core.config
from db.db_engine import async_session
from db.db_models import UserConfList, WgConfList, ServerConf
from utils.command_executor import execute_command
from utils.config_manager import ConfigManager
from utils.send_msg import send_message_to_user


class SubscriptionManager:
    """Класс для управления подписками пользователей и конфигурацией WireGuard."""

    @staticmethod
    async def _get_users_with_expiring_subscriptions():
        """Получает список пользователей с подписками, истекающими через 2 дня."""
        now = datetime.now()
        warning_date = now + timedelta(days=2)

        async with async_session() as session:
            result = await session.execute(
                select(UserConfList.user_id)
                .join(WgConfList, UserConfList.conf_id == WgConfList.conf_id)
                .where(WgConfList.valid_until < warning_date, WgConfList.valid_until > now)
            )
            return result.scalars().all()

    @staticmethod
    async def notify_users_about_expiring_subscriptions():
        """Уведомляет пользователей с истекающими подписками."""
        users_to_warn = await SubscriptionManager._get_users_with_expiring_subscriptions()

        for user_id in users_to_warn:
            await send_message_to_user(user_id, "⚠️ Ваша подписка истекает. Пожалуйста, продлите её.")

    @staticmethod
    async def _get_users_with_expired_subscriptions():
        """Получает список пользователей с истекшими подписками."""
        now = datetime.now()

        async with async_session() as session:
            result = await session.execute(
                select(UserConfList.user_id)
                .join(WgConfList, UserConfList.conf_id == WgConfList.conf_id)
                .where(WgConfList.valid_until < now, WgConfList.is_active == True)
            )
            return result.scalars().all()

    @staticmethod
    async def deactivate_expired_subscriptions():
        """Отключает пользователей с истекшими подписками и обновляет статус услуг."""
        expired_users = await SubscriptionManager._get_users_with_expired_subscriptions()

        async with async_session() as session:
            for user_id in expired_users:
                await send_message_to_user(user_id, "❌ Ваша подписка истекла. VPN отключен.")

                await session.execute(
                    update(WgConfList)
                    .where(
                        WgConfList.conf_id.in_(
                            select(UserConfList.conf_id).where(UserConfList.user_id == user_id)
                        )
                    )
                    .values(is_active=False)
                )

            await session.commit()

    @staticmethod
    async def update_wireguard_config():
        """Обновляет конфигурацию WireGuard."""
        async with async_session() as session:
            conf = (await session.execute(select(ServerConf))).scalars().first()

            server_config = await ConfigManager.get_server_config(
                conf.private_key, conf.allowed_ips, conf.listen_port,
                conf.pre_up, conf.post_up, conf.pre_down, conf.post_down
            )

            active_users = (await session.execute(
                select(WgConfList).where(WgConfList.is_active == True)
            )).scalars().all()

            for user in active_users:
                server_config += await ConfigManager.get_peer_config(
                    user.conf_id, user.public_key, user.preshared_key, user.allowed_ips
                ) + "\n"

            with open(core.config.config.wg_config_path, "w") as f:
                f.write(server_config)

        await execute_command("wg syncconf wg0 <(wg-quick strip wg0)")

    @classmethod
    async def check_expiring_subscriptions_and_notify_users(cls):
        """Основная функция: проверяет подписки и выполняет нужные действия."""
        await cls.notify_users_about_expiring_subscriptions()
        await cls.deactivate_expired_subscriptions()
        await cls.update_wireguard_config()
