from aiogram.utils.keyboard import InlineKeyboardButton,InlineKeyboardMarkup
kb = [
    [InlineKeyboardButton(text="🟢30 дней - 170 ₽ - 🍔",callback_data='ext_1_month')],
    [InlineKeyboardButton(text="🟡60 дней - 310 ₽ - 🍕",callback_data='ext_2_months')],
    [InlineKeyboardButton(text="🔴90 дней - 430 ₽ - 🍿",callback_data='ext_3_months')],
    [InlineKeyboardButton(text="🟣180 дней - 690 ₽ - 🥃",callback_data='ext_6_months')],
    [InlineKeyboardButton(text="🔵365 дней - 1100 ₽ - 🍾",callback_data='ext_1_year')],
]

select_extension_keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
