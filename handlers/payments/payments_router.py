from datetime import timedelta

from aiogram import Router,F
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from commands.manage_config import ManageWireGuardConfig
from states.buying_state import BuyVPNState
from states.extend_state import ExtendVPNState

TARIFFS = {
    "1_month": timedelta(days=30),
    "2_months": timedelta(days=60),
    "3_months": timedelta(days=90),
    "6_months": timedelta(days=180),
    "1_year": timedelta(days=365)
}


router = Router()

@router.message(StateFilter(ExtendVPNState.success_payment),F.successful_payment)
async def handle_payment(message: Message,state: FSMContext):
    """Обработка успешной покупки продления услуги"""
    payload = message.successful_payment.invoice_payload
    if payload.startswith("ext_"):
        duration = TARIFFS.get(payload.replace("ext_",""))
        if duration:
            user_data = await state.get_data()
            service_id = user_data.get("service_id")
            await ManageWireGuardConfig.renew_wireguard_config(message,service_id, duration)

    await state.clear()


@router.message(StateFilter(BuyVPNState.success_payment),F.successful_payment)
async def handle_payment(message: Message,state: FSMContext):
    """Обработки успешной покупки выбранного тарифа VPN"""
    payload = message.successful_payment.invoice_payload
    if payload.startswith("new_"):
        duration = TARIFFS.get(payload.replace("new_", ""))
        if duration:
            await ManageWireGuardConfig.add_wireguard_config(message, duration)

    await state.clear()