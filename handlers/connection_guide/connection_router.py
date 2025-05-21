from aiogram import Router, F
from aiogram.types import Message

from keyboards.connection_guide_kbd.faq_keyboard import faq_keyboard
from keyboards.main_keyboard.start_kb import start_keyboard

router = Router()


@router.message(F.text == '📚 Помощь и FAQ')
async def faq_guide(message: Message):
    await message.answer("Здесь вы найдёте ответы на популярные вопросы и инструкции по настройке VPN.",
                         reply_markup=faq_keyboard)


@router.message(F.text == 'ℹ️ Общая информация')
async def general_info_guide(message: Message):
    msg = """❓ Что такое WireGuard?
WireGuard — это современный VPN-протокол, который обеспечивает высокую скорость, безопасность и простоту настройки.

💰 Какие тарифы доступны?
Вы можете выбрать различные тарифные планы в зависимости от ваших потребностей. Подробности можно посмотреть в меню "🚀 Оформить подписку".

🔄 Как продлить подписку?
Перейдите в раздел "🌐 Продлить подписку", выберите нужную услугу и оплатите продление.
"""
    await message.answer(msg)


@router.message(F.text == '⚙️ Настройка и подключение VPN')
async def connection_guide(message: Message):
    msg = """1️⃣ Установка WireGuard
💻 Windows/macOS: Официальный сайт
📱 Android: Google Play
🍏 iOS: App Store
🐧 Linux: Установите через пакетный менеджер (apt, dnf, pacman).

2️⃣ Покупка и получение конфигурации
После оплаты получите файл .conf для подключения.

3️⃣ Добавление конфигурации
📂 Импорт файла: Откройте WireGuard → «Добавить туннель» → «Импортировать из файла» → Выберите .conf.

4️⃣ Подключение
Откройте WireGuard → Выберите профиль → «Подключиться» ✅.

5️⃣ Проверка
Перейдите на ipleak.net или whoer.net, чтобы убедиться, что IP изменился.

🎉 VPN готов к работе! Отключить можно в WireGuard → «Отключить»."""
    await message.answer(msg)

@router.message(F.text == '🛠 Решение проблем')
async def problem_solving_guide(message: Message):
    msg = """⚠️ VPN не работает?
1️⃣ Проверьте, включено ли соединение в WireGuard.
2️⃣ Убедитесь, что интернет работает.
3️⃣ Перезагрузите устройство.
4️⃣ Если проблема осталась – обратитесь в поддержку.

📶 Как проверить скорость VPN?

Speedtest → speedtest.net

Fast → fast.com"""
    await message.answer(msg)

@router.message(F.text == '📩 Поддержка')
async def contact_support(message: Message):
    msg = """Если у вас остались вопросы или нужна помощь, нажмите "🛠 Связаться с нами" и опишите проблему.
🎯 Ваш комфорт – наш приоритет! 🚀"""
    await message.answer(msg)


@router.message(F.text == 'Главное меню  ↩️')
async def back_to_main_menu(message:Message):
    await message.answer(
        f"Приветствуем, <a href='tg://user?id={message.from_user.id}'>{message.from_user.username}</a>😉\n⏩ Выберите требуемый раздел из меню",
        reply_markup=start_keyboard, parse_mode="HTML")