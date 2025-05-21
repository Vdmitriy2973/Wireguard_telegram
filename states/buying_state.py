from aiogram.fsm.state import State, StatesGroup

class BuyVPNState(StatesGroup):
    """Покупка конфигурации VPN"""
    choosing_vpn_tariff = State() # Выбор тарифа VPN
    waiting_payment = State() # Ожидание оплаты тарифа
    success_payment = State() # Успешная оплата тарифа