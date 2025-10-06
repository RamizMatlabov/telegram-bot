import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Import handlers
from handlers.start import router as start_router
from handlers.menu import router as menu_router
from handlers.admin import router as admin_router
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Определяем режим работы (webhook или polling)
WEBHOOK_MODE = os.getenv('WEBHOOK_MODE', 'False').lower() == 'true'
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '/webhook')
APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
APP_PORT = int(os.getenv('PORT', 8080))
DELETE_WEBHOOK_ON_STARTUP = os.getenv('DELETE_WEBHOOK_ON_STARTUP', 'False').lower() == 'true'

async def delete_webhook(bot: Bot) -> None:
    """Принудительное удаление вебхука"""
    try:
        logger.info("Deleting webhook...")
        await bot.delete_webhook()
        logger.info("Webhook deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")

async def on_startup(bot: Bot) -> None:
    """Настройка вебхука при запуске"""
    # Сначала удаляем вебхук, если это требуется
    if DELETE_WEBHOOK_ON_STARTUP:
        await delete_webhook(bot)
    
    # Затем устанавливаем новый вебхук, если нужно
    if WEBHOOK_MODE and WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)
        logger.info(f"Webhook set to {WEBHOOK_URL + WEBHOOK_PATH}")

async def on_shutdown(bot: Bot) -> None:
    """Удаление вебхука при остановке"""
    if WEBHOOK_MODE:
        await bot.delete_webhook()
    await bot.session.close()
    logger.info("Bot shutdown complete")

async def main():
    """Main function to start the bot"""
    # Initialize bot and dispatcher
    bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Register routers
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(admin_router)

    # Регистрируем обработчики запуска и остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Запускаем бота в нужном режиме
    if WEBHOOK_MODE:
        # Настройка веб-сервера для вебхука
        app = web.Application()
        
        # Настройка обработчика вебхуков
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        
        # Настройка веб-приложения
        setup_application(app, dp, bot=bot)
        
        # Запуск веб-сервера
        logger.info(f"Starting webhook on {APP_HOST}:{APP_PORT}")
        try:
            web.run_app(app, host=APP_HOST, port=APP_PORT)
        except Exception as e:
            logger.error(f"Error starting webhook: {e}")
    else:
        # Запуск в режиме polling
        logger.info("Starting bot in polling mode...")
        try:
            await dp.start_polling(bot)
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    try:
        if WEBHOOK_MODE:
            # В режиме вебхука используем aiohttp
            asyncio.run(main())
        else:
            # В режиме поллинга используем asyncio
            asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")