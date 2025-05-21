from aiogram.utils.keyboard import InlineKeyboardButton,InlineKeyboardMarkup

async def get_personal_services_to_extend_keyboard(services_set:list):
    kb = []
    for config in services_set:
        kb.append([InlineKeyboardButton(text=f"🛜{config[0]}",callback_data="renew_"+config[0])])


    return InlineKeyboardMarkup(inline_keyboard=kb)

