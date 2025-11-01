import logging
import asyncio
from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN, validate_config
from handlers.start import router as start_router
from handlers.buckets import router as buckets_router
from handlers.faces import router as faces_router
from handlers.search import router as search_router
from handlers.messages import router as messages_router
from handlers.callbacks import router as callbacks_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    # Проверка конфигурации
    try:
        validate_config()
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        return

    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация роутеров
    routers = [
        start_router,
        buckets_router, 
        faces_router,
        search_router,
        messages_router,
        callbacks_router
    ]
    
    for router in routers:
        dp.include_router(router)

    logging.info("Bot started")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot stopped with error: {e}")

if __name__ == "__main__":
    asyncio.run(main())