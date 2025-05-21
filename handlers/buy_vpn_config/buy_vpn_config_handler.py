from datetime import timedelta
from aiogram.filters.state import StateFilter
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery
from sqlalchemy import select, update

from commands.manage_config import ManageWireGuardConfig
from db.db_engine import async_session
from db.db_models import UserList, WgConfList
from bot import bot
from states.buying_state import BuyVPNState

router = Router()

# 🔹 Тарифные планы
TARIFFS = {
    "new_1_month": ("Доступ к WireGuard на 1 месяц", 99),
    "new_2_months": ("Доступ к WireGuard на 2 месяца", 139),
    "new_3_months": ("Доступ к WireGuard на 3 месяца", 179),
    "new_6_months": ("Доступ к WireGuard на 6 месяцев", 279),
    "new_1_year": ("Доступ к WireGuard на 1 год", 539),
}


@router.callback_query(F.data == "demo")
async def receive_demo_tariff(callback: CallbackQuery):
    """Выдать демо-версию VPN"""
    async with async_session() as session:
        res = await session.scalar(select(UserList).where(UserList.user_id == callback.message.chat.id))

        if res and res.used_demo:
            return await callback.message.answer("Вы уже использовали ДЕМО-версию!")

        await session.execute(
            update(UserList).where(UserList.user_id == callback.message.chat.id).values(used_demo=True))
        await session.commit()

    await ManageWireGuardConfig.add_wireguard_config(callback.message, timedelta(days=2))


@router.callback_query(StateFilter(BuyVPNState.choosing_vpn_tariff),F.data.in_(TARIFFS.keys()))
async def receive_tariff(callback: CallbackQuery,state:FSMContext):
    """Обработчик оплаты VPN (любой тариф)"""
    title, price = TARIFFS[callback.data]
    await state.set_state(BuyVPNState.waiting_payment)
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Оплата услуги",
        description=f"{title}. Конфигурационный файл .conf для программы WireGuard.",
        payload=callback.data,
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Оплата услуги", amount=price)],
    )




@router.pre_checkout_query(StateFilter(BuyVPNState.waiting_payment),F.invoice_payload.startswith("new_"))
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery,state:FSMContext):
    """Проверка перед оплатой"""
    async with async_session() as session:
        result = await session.execute(select(WgConfList.allowed_ips))
        pull_ip_addresses = result.scalars().all()

    for num in range(2, 254):
        for i in range(2, 254):
            if f"10.8.{num}.{i}" not in pull_ip_addresses:
                await state.set_state(BuyVPNState.success_payment)
                return await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


    await state.clear()
    await bot.answer("Нет доступных IP-адресов, попробуйте позже")
