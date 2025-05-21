import subprocess

from core.config import config


class ConfigManager:
    @staticmethod
    async def get_peer_config(name: str, public_key: str, preshared_key: str, ip: str) -> str:
        """Создать конфигурацию Peer'а WireGuard
        :param name: Имя клиента
        :param public_key: Публичный ключ клиента
        :param preshared_key: доп. ключ шифрования клиента
        :param ip: IP-адрес клиента
        """
        return f"""# {name}
[Peer]
PublicKey = {public_key}
PresharedKey = {preshared_key}
AllowedIPs = {ip}/32
"""

    @staticmethod
    async def get_client_config(private_key: str, ip: str, preshared_key: str) -> str:
        """Создать конфигурационный файл клиента WireGuard
        :param private_key: Приватный ключ клиента
        :param ip: IP-адрес клиента
        :param preshared_key: доп. ключ шифрования клиента
        """
        # QfG/GHueNSweNReeLzZfgejUD8h6L0oBuKGrMZUViVU=
	# PublicKey = {subprocess.check_output(f'wg show {config.wg_interface} public-key', shell=True).decode().strip()}
        return f"""[Interface]
PrivateKey = {private_key}
Address = {ip}
DNS = 8.8.4.4
[Peer] 
PublicKey = QfG/GHueNSweNReeLzZfgejUD8h6L0oBuKGrMZUViVU=
PresharedKey = {preshared_key}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 0
Endpoint = {config.server_public_ip}:{config.server_port}
"""

    @staticmethod
    async def get_server_config(private_key: str, ip: str, listen_port: int, pre_up: str, post_up: str,
                                pre_down: str, post_down: str) -> str:
        """Создать конфигурацию сервера WireGuard
        :param private_key: Приватный ключ клиента
        :param ip: IP-адрес сервера
        :param listen_port: Порт, который слушает сервер
        :param pre_up:
        :param post_up:
        :param pre_down:
        :param post_down
        """
        return f"""[Interface]
PrivateKey = {private_key}
Address = {ip}
ListenPort = {listen_port}
PreUp = {pre_up}
PostUp = {post_up}
PreDown = {pre_down}
PostDown = {post_down}
"""

