import os

from dotenv import load_dotenv
load_dotenv()


server_config = {
    "PrivateKey": os.getenv("PrivateKey"),
    "Address": os.getenv("Address"),
    "ListenPort": os.getenv("ListenPort"),
    "PreUp": "",
    "PostUp": os.getenv("PostUp"),
    "PreDown": "",
    "PostDown": ""

}

config = {
    "dns_server": os.getenv("dns_server"),
    "BOT_TOKEN" : os.getenv("BOT_TOKEN"),
    "server_socket" : os.getenv("server_socket"),
    "PersistentKeepalive": os.getenv("PersistentKeepalive"),

    "wg_interface" : os.getenv("wg_interface"),
    "wg_config_path" : os.getenv("wg_config_path")
}

if not config or not server_config:
    raise Exception("File .env wasn't found")
