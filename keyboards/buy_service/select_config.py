from aiogram.utils.keyboard import InlineKeyboardButton,InlineKeyboardMarkup
kb = [
    [InlineKeyboardButton(text="🚀 Получить бесплатную ДЕМО версию (2 дня)",callback_data='demo')],
    [InlineKeyboardButton(text="🟢30 дней - 170 ₽ - 🍔 (99 🌟)",callback_data='new_1_month')],
    [InlineKeyboardButton(text="🟡60 дней - 310 ₽ - 🍕 (139 🌟)",callback_data='new_2_months')],
    [InlineKeyboardButton(text="🔴90 дней - 430 ₽ - 🍿 (179 🌟)",callback_data='new_3_months')],
    [InlineKeyboardButton(text="🟣180 дней - 690 ₽ - 🥃 (279 🌟)",callback_data='new_6_months')],
    [InlineKeyboardButton(text="🔵365 дней - 1100 ₽ - 🍾 (539 🌟)",callback_data='new_1_year')],
]

select_vpn_tariff_keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

