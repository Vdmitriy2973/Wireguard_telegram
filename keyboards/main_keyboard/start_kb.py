from aiogram.utils.keyboard import KeyboardButton,ReplyKeyboardMarkup
kb = [
    [KeyboardButton(text="🚀 Оформить подписку"),KeyboardButton(text="🌐 Продлить подписку")],
    [KeyboardButton(text="🗄 Мои услуги")],
    [KeyboardButton(text="📚 Помощь и FAQ")]
]

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=kb)

