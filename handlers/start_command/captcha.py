import random

from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
EMOJIS = ['🟦', '🟨', '🟪', '🟩', '🟥', '🟧', '🟫', '⬜️', '⬛️']


async def generate_captcha():
    """Генерирует случайную капчу с эмодзи."""
    correct_emoji = random.choice(EMOJIS)

    # Создаём inline-клавиатуру

    shuffled_emojis = random.sample(EMOJIS, len(EMOJIS))  # Перемешиваем список эмодзи
    keyboard = [
        [InlineKeyboardButton(text=shuffled_emojis[i], callback_data="captcha:"+correct_emoji+":"+shuffled_emojis[i]) for i in range(j, j + 3)]
        for j in range(0, len(shuffled_emojis), 3)
    ]
    keyboard = InlineKeyboardMarkup(row_width=3,inline_keyboard=keyboard)

    return correct_emoji, keyboard