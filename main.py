import asyncio
from datetime import datetime, timedelta

import handlers
from bot import bot,dp
from db.db_engine import init_db
from utils import subscription_checker


async def daily_subscription_checker():
    while True:
        # Вызываем проверку подписок
        await subscription_checker.SubscriptionManager.check_expiring_subscriptions_and_notify_users()

        # Получаем текущее время
        now = datetime.now()

        # Вычисляем время до следующего запуска (через 24 часа)
        next_run = now + timedelta(days=1)

        # Рассчитываем количество секунд до следующего запуска
        seconds_until_next_run = (next_run - now).total_seconds()

        # Ждем до следующего запуска
        await asyncio.sleep(seconds_until_next_run)


async def main():
    await init_db()
    dp.include_router(handlers.main_router)
    asyncio.create_task(daily_subscription_checker())
    await dp.start_polling(bot, close_bot_session=True)


if __name__ == "__main__":
    print("Bot has been started")
    asyncio.run(main())
