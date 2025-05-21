from aiogram import Router, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from db.db_engine import async_session
from db.db_models import UserConfList, WgConfList
from keyboards.get_my_services.user_services import get_personal_services_keyboard
from utils.config_manager import ConfigManager

router = Router()


@router.message(F.text == '🗄 Мои услуги')
async def get_personal_services(message: Message):
    async with async_session() as session:
        stmt = (
            select(
                WgConfList.conf_id
            )
            .join(UserConfList, UserConfList.conf_id == WgConfList.conf_id)
            .where(UserConfList.user_id == message.from_user.id)
        )

        services = (await session.execute(stmt)).all()

    if len(services) < 1:
        return await message.answer("У вас нет приобретенных услуг!")
    kb = await get_personal_services_keyboard(services)
    await message.answer("Выберите услугу для получения информации", parse_mode=ParseMode.HTML, reply_markup=kb)


@router.callback_query(F.data.startswith('conf'))
async def get_current_service(callback: CallbackQuery):
    async with async_session() as session:
        stmt = (
            select(WgConfList)
            .where(WgConfList.conf_id == callback.data)
        )

        service = (await session.execute(stmt)).scalars().first()

    await callback.message.answer(f"Услуга действительно до {service.valid_until}\n\n" +
                                  await ConfigManager.get_client_config(service.private_key, service.allowed_ips,
                                                                        service.preshared_key))
