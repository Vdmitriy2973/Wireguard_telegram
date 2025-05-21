from aiogram.utils.keyboard import InlineKeyboardButton,InlineKeyboardMarkup

async def get_personal_services_keyboard(services_set:list):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"🛜{config[0]}",callback_data=config[0])] for config in services_set])

