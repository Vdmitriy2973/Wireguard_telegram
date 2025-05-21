from config import config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=config["BOT_TOKEN"], storage=MemoryStorage())
dp = Dispatcher()
