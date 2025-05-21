from aiogram.fsm.state import State, StatesGroup

class ExtendVPNState(StatesGroup):
    """Продление приобретённой услуги"""
    choosing_service = State() # Выбор приобретённой услуги
    choosing_tariff = State() # Выбор срока продления услуги (1 месяц, 2 месяца и т.д.)
    waiting_payment = State() # Ожидание оплаты
    success_payment = State() # Успешная оплата
