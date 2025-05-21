from aiogram.utils.keyboard import KeyboardButton,ReplyKeyboardMarkup
kb = [
    [KeyboardButton(text="ℹ️ Общая информация")],
    [KeyboardButton(text="⚙️ Настройка и подключение VPN")],
    [KeyboardButton(text="🛠 Решение проблем")],
    [KeyboardButton(text="📩 Поддержка")],
    [KeyboardButton(text="Главное меню  ↩️")]
]

faq_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=kb)

