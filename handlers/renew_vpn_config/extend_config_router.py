from datetime import timedelta

from aiogram import Router, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from sqlalchemy import select

from db.db_engine import async_session
from db.db_models import UserConfList, WgConfList
from keyboards.extend_my_services.extend_vpn import get_personal_services_to_extend_keyboard
from keyboards.extend_my_services.extension_options import select_extension_keyboard
from bot import bot
from states.extend_state import ExtendVPNState

router = Router()

TARIFFS = {
    "ext_1_month": ("Продление доступа к WireGuard на 1 месяц", 99),
    "ext_2_months": ("Продление доступа к WireGuard на 2 месяца", 139),
    "ext_3_months": ("Продление доступа к WireGuard на 3 месяца", 179),
    "ext_6_months": ("Продление доступа к WireGuard на 6 месяцев", 279),
    "ext_1_year": ("Продление доступа к WireGuard на 1 год", 539),
}


@router.message(F.text == '🌐 Продлить подписку')
async def get_personal_services_to_extend(message: Message, state: FSMContext):
    async with async_session() as session:
        services = (await session.execute(
            select(
                WgConfList.conf_id
            )
            .join(UserConfList, UserConfList.conf_id == WgConfList.conf_id)
            .where(UserConfList.user_id == message.from_user.id)
        )).all()
    if len(services) < 1:
        return await message.answer("У вас нет приобретенных услуг!")
    kb = await get_personal_services_to_extend_keyboard(services)

    await state.set_state(ExtendVPNState.choosing_service)
    await message.answer("Выберите услугу, которую вы хотите продлить!", parse_mode=ParseMode.HTML, reply_markup=kb)


@router.callback_query(StateFilter(ExtendVPNState.choosing_service), F.data.startswith("renew_"))
async def extend_service(callback: CallbackQuery, state: FSMContext):
    await state.update_data(service_id=callback.data.replace("renew_", ""))
    await callback.message.answer("Выберите удобный вариант продления", reply_markup=select_extension_keyboard)
    await state.set_state(ExtendVPNState.choosing_tariff)


@router.callback_query(StateFilter(ExtendVPNState.choosing_tariff), F.data.startswith("ext_"))
async def receive_tariff(callback: CallbackQuery, state: FSMContext):
    """Обработчик оплаты VPN (любой тариф)"""

    user_data = await state.get_data()
    service_id = user_data.get("service_id")

    if not service_id:
        return await callback.message.answer("Ошибка! Попробуйте снова.")
    title, price = TARIFFS[callback.data]
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Оплата услуги",
        description=f"{title}. Конфигурационный файл .conf для программы WireGuard.",
        payload=callback.data,
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Оплата услуги", amount=price)],
    )

    await state.set_state(ExtendVPNState.waiting_payment)


@router.pre_checkout_query(StateFilter(ExtendVPNState.waiting_payment), F.invoice_payload.startswith("ext_"))
async def process_renew_service_payment(pre_checkout_query: PreCheckoutQuery, state: FSMContext):
    """Проверка перед оплатой продления услуги"""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.set_state(ExtendVPNState.success_payment)
