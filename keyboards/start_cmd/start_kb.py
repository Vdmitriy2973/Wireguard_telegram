from aiogram.utils.keyboard import KeyboardButton,ReplyKeyboardMarkup
kb = [
    [KeyboardButton(text="🚀 Оформить подписку"),KeyboardButton(text="🔁 Продлить подписку")],
    [KeyboardButton(text="🗄 Мои услуги")],
    [KeyboardButton(text="🔧 Инструкция по подключению VPN через WireGuard")]
]

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=kb)

