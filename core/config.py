from dataclasses import dataclass

@dataclass
class Config:
    server_public_ip = "185.119.196.168"
    server_port = 972
    wg_interface = "wg0"
    wg_db = 'postgres'
    wg_config_path = "/etc/wireguard/wg0.conf"



config = Config()