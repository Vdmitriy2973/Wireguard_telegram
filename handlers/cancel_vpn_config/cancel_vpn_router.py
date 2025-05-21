from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message
from bot import bot

router = Router()


@router.message(Command("refund"))
async def cmd_refund(
    message: Message,
):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Использование: /refund <ID транзакции>")

    transaction_id = args[1]
    try:
        await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id
        )
        await message.answer(
            "refund-successful"
        )
    except TelegramBadRequest as error:
        if "CHARGE_ALREADY_REFUNDED" in error.message:
            text = "refund-already-refunded"
        else:
            text = "refund-code-not-found"
        await message.answer(text)
        return