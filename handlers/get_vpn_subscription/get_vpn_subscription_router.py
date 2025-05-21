from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from commands.manage_config import ManageWireGuardConfig
from keyboards.buy_service.select_config import select_vpn_tariff_keyboard
from states.buying_state import BuyVPNState

router = Router()


@router.message(F.text == '🚀 Оформить подписку')
async def get_vpn_subscription(message: Message,state:FSMContext):

    await state.set_state(BuyVPNState.choosing_vpn_tariff)
    await message.answer("""Оформляя подписку на WireGuard, вы получаете: 👇
└ 🚀 Высокую скорость и надежное соединение
└ ✅ Неограниченный трафик
└ 🔕 Отсутствие рекламы
└ ⛔️ Без скрытых автосписаний

💡 Лайфхак: Чем длиннее период подписки, тем ниже стоимость в месяц! 😉

🔹 Как подключиться?
1️⃣ Выберите подходящий тариф ниже 👇🏻
2️⃣ Оплатите подписку
3️⃣ Загрузите полученный файл в приложение WireGuard

❗️После оплаты вы получите конфигурационный файл, который необходимо импортировать в WireGuard.""",
                         reply_markup=select_vpn_tariff_keyboard)


@router.message(Command("remove"))
async def remove_conf(message: Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Использование: /remove <название_конфигурации>")

    client_name = args[1]

    return await ManageWireGuardConfig.remove_peer(message, client_name)
