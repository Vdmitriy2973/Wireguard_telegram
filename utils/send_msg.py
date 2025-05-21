from bot import bot


async def send_message_to_user(user_id: int, text: str):
    """Отправить сообщение пользователю
    :param user_id: ID пользователя Telegram
    :param text: Отправляемый текст"""
    await bot.send_message(chat_id=user_id, text=text)