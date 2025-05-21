import tempfile
from datetime import datetime, timedelta

from aiogram.types import Message, BufferedInputFile
from pytz import timezone
from sqlalchemy import insert, select, delete, cast, Date, update

import core
from core.config import config
from db.db_engine import async_session
from db.db_models import WgConfList, ServerConf, UserConfList
from utils.config_manager import ConfigManager
from utils.command_executor import execute_command


class ManageWireGuardConfig:
    @staticmethod
    async def add_wireguard_config(message: Message, period: timedelta):
        """Добавить конфигурацию Peer'а WireGuard"""
        async with async_session() as session:
            result = await session.execute(select(WgConfList.allowed_ips))
            pull_ip_addresses = result.scalars().all()

        found_ip = False
        name = ''
        ip = ''
        for num in range(2, 254):
            for i in range(2, 254):
                ip = f"10.8.{str(num)}.{str(i)}"
                if f"{ip}" not in pull_ip_addresses:
                    name = f"conf{str(num)}_{str(i)}"
                    found_ip = True
                    break
            if found_ip:
                break
        else:
            return await message.answer(f"Произошла непредвиденная ошибка, повторите ошибку позже")

        private_key, _ = await execute_command("wg genkey")
        public_key, _ = await execute_command(f"echo {private_key} | wg pubkey")
        preshared_key, _ = await execute_command(f"wg genpsk")
        valid_until = (datetime.now(timezone('Europe/Moscow')) + period).date()

        async with async_session() as session:
            await session.execute(insert(WgConfList).values(
                conf_id=name,
                public_key=public_key,
                private_key=private_key,
                preshared_key=preshared_key,
                allowed_ips=ip,
                valid_until=cast(valid_until, Date)),
            )

            await session.execute(insert(UserConfList).values(
                conf_id=name,
                user_id=message.chat.id
            ))
            await session.commit()

        peer_config = await ConfigManager.get_peer_config(name, public_key, preshared_key, ip)
        client_conf = await ConfigManager.get_client_config(private_key, ip, preshared_key)

        with open(config.wg_config_path, "a") as f:
            f.write(peer_config)
        await execute_command("wg syncconf wg0 <(wg-quick strip wg0)")

        await message.answer(f"🕒Конфигурация действительна до {valid_until}")
        await message.answer("Cкачайте файл с настройками и загрузите его в приложение WireGuard.")
        with tempfile.TemporaryFile(mode="w+", suffix=".txt") as temp_file:
            temp_file.write(client_conf)
            temp_file.flush()
            temp_file.seek(0)

            file_data = temp_file.read()
            file_name = str(message.chat.id) + ".conf"
            file = BufferedInputFile(file_data.encode(), filename=file_name)
            await message.answer_document(file)

        await message.answer("Либо используйте детальные настройки")
        await message.answer(client_conf)

    @staticmethod
    async def remove_peer(message: Message, name: str):
        """Удалить Peer'а из WireGuard конфигурации по названию услуги.
        :param message: Message object
        :param name: Имя клиента
        """

        async with async_session() as session:
            r = await session.execute(delete(WgConfList).where(WgConfList.conf_id == name))

            if r.rowcount < 1:
                return await message.answer("❌ Конфигурация с таким названием не была найдена!")

            await session.commit()

            users_conf = (await session.execute(select(WgConfList))).scalars().all()

            conf = (await session.execute(select(ServerConf))).scalars().first()

        users = [cfg for cfg in users_conf]

        server_config = await ConfigManager.get_server_config(conf.private_key, conf.allowed_ips,
                                                              conf.listen_port,
                                                              conf.pre_up, conf.post_up,
                                                              conf.pre_down, conf.post_down)
        for user_conf in users:
            server_config += await ConfigManager.get_peer_config(user_conf.conf_id, user_conf.public_key,
                                                                 user_conf.preshared_key, user_conf.allowed_ips) + "\n"

        with open(core.config.config.wg_config_path, "w") as f:
            f.write(server_config)

        await execute_command("wg syncconf wg0 <(wg-quick strip wg0)")

        return await message.answer(f"✅ Конфигурация удалёна! Средства были возвращены")

    @staticmethod
    async def renew_wireguard_config(message: Message, conf_id: str, duration: timedelta):
        async with async_session() as session:
            # Получаем текущее значение valid_until
            result = await session.execute(select(WgConfList).filter(WgConfList.conf_id == conf_id))
            config = result.scalars().first()

            if config:
                current_valid_until = config.valid_until

                # Если valid_until уже меньше текущего времени, добавляем новое время
                if current_valid_until < datetime.now():
                    new_valid_until = datetime.now() + duration
                else:
                    new_valid_until = current_valid_until + duration

                # Обновляем колонку valid_until
                await session.execute(
                    update(WgConfList)
                    .where(WgConfList.conf_id == conf_id)
                    .values(valid_until=new_valid_until, is_active=True)
                )
                await session.commit()
                return await message.answer(
                    f"Ваша VPN-услуга успешно продлена! Новый срок действия конфигурации: {new_valid_until}.")

            return await message.answer("Конфигурация не найдена")
