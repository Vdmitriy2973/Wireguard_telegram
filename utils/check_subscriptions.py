from datetime import datetime, timedelta

from sqlalchemy import select, update

import core
from core.config import config
from db.db_engine import async_session
from db.db_models import UserConfList, WgConfList, ServerConf
from utils.create_config import ConfigManager
from utils.exec_cmd import execute_command
from utils.send_msg import send_message_to_user


async def check_and_notify_users():
    """Проверите пользователей с истекающей/истекшими подписками"""

    now = datetime.now()
    warning_date = now + timedelta(days=2)
    removing_date = now - timedelta(days=10)

    async with async_session() as session:
        # Выбираем пользователей, у которых подписка истекает через 2 дня
        result = await session.execute(
            select(UserConfList.user_id)
            .join(WgConfList, UserConfList.conf_id == WgConfList.conf_id)
            .where(WgConfList.valid_until < warning_date, WgConfList.valid_until > now)
        )
        users_to_warn = result.scalars().all()

        for user_id in users_to_warn:
            await send_message_to_user(user_id, "⚠️ Ваша подписка истекает. Пожалуйста, продлите её.")

        # Выбираем пользователей с истекшей подпиской
        result = await session.execute(
            select(UserConfList.user_id)
            .join(WgConfList, UserConfList.conf_id == WgConfList.conf_id)
            .where(WgConfList.valid_until < now)
        )
        expired_users = result.scalars().all()
        for user_id in expired_users:
            await send_message_to_user(user_id, "❌ Ваша подписка истекла. VPN отключен.")

            # Делаем услугу неактивной
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

        conf = (await session.execute(select(ServerConf))).scalars().first()
        server_config = await ConfigManager.get_server_config(conf.private_key, conf.allowed_ips,
                                                              conf.listen_port,
                                                              conf.pre_up, conf.post_up,
                                                              conf.pre_down, conf.post_down)

        active_users = (await session.execute(select(WgConfList).where(WgConfList.is_active == True))).scalars().all()
        active_users = [cfg for cfg in active_users]

        for user in active_users:
            server_config += await ConfigManager.get_peer_config(user.conf_id, user.public_key,
                                                                 user.preshared_key, user.allowed_ips) + "\n"

        with open(core.config.config.wg_config_path, "w") as f:
            f.write(server_config)

        await execute_command("wg syncconf wg0 <(wg-quick strip wg0)")

        await session.commit()
