from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from pytz import timezone
from sqlalchemy import insert, select

from db.db_engine import async_session
from db.db_models import UserList
from handlers.start_command.captcha import generate_captcha
from keyboards.main_keyboard.start_kb import start_keyboard

router = Router()


@router.callback_query(lambda c: c.data.startswith("captcha"))
async def process_captcha(callback: CallbackQuery):
    _, correct_emoji, chosen_emoji = callback.data.split(":")

    if chosen_emoji == correct_emoji:
        async with async_session() as session:
            await session.execute(insert(UserList).values(
                user_id=callback.message.chat.id,
                username=callback.message.chat.username,
                register_date=str(datetime.now(timezone("Europe/Moscow"))),
                used_demo=False,
            ))
            await session.commit()
        await callback.message.answer("🎉 Вы успешно прошли капчу!")
        await callback.message.answer(
            f"Приветствуем, <a href='tg://user?id={callback.message.from_user.id}'>{callback.message.from_user.username}</a>😉\n⏩ Выберите требуемый раздел из меню",
            reply_markup=start_keyboard, parse_mode="HTML")
    else:
        await callback.message.answer("❌ Неверно, попробуйте ещё раз.")
        correct_emoji, keyboard = await generate_captcha()
        await callback.message.answer(f"Выберите цвет: {correct_emoji}",
                                      reply_markup=keyboard)


@router.message(CommandStart())
async def start(message: Message):
    async with async_session() as session:
        user = (await session.execute(select(UserList).where(
            UserList.user_id == message.from_user.id
        ))).all()
    if not user:
        correct_emoji, keyboard = await generate_captcha()
        await message.answer(f"Выберите цвет: {correct_emoji}", reply_markup=keyboard)
    else:
        await message.answer(
            f"Приветствуем, <a href='tg://user?id={message.from_user.id}'>{message.from_user.username}</a>😉\n⏩ Выберите требуемый раздел из меню",
            reply_markup=start_keyboard, parse_mode="HTML")
