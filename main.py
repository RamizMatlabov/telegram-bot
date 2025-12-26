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
from handlers.cart import router as cart_router
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Определяем режим работы (webhook или polling)
# Если мы на Render (определяется по RENDER_EXTERNAL_URL), автоматически включаем webhook
IS_RENDER = bool(os.getenv('RENDER_EXTERNAL_URL'))
WEBHOOK_MODE_ENV = os.getenv('WEBHOOK_MODE', 'False')
# На Render всегда используем webhook режим, если не указано иное
if IS_RENDER and WEBHOOK_MODE_ENV.lower() not in ('false', '0', 'no'):
    WEBHOOK_MODE = True
    logger.info("Detected Render environment, enabling webhook mode")
else:
    WEBHOOK_MODE = WEBHOOK_MODE_ENV.lower() in ('true', '1', 'yes')

WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '/webhook')
APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
# Render автоматически устанавливает PORT, используем его или дефолтный 10000
APP_PORT = int(os.getenv('PORT', os.getenv('RENDER_PORT', '10000')))
DELETE_WEBHOOK_ON_STARTUP = os.getenv('DELETE_WEBHOOK_ON_STARTUP', 'False').lower() in ('true', '1', 'yes')

# Логируем настройки для отладки
logger.info(f"IS_RENDER: {IS_RENDER}")
logger.info(f"WEBHOOK_MODE env value: {WEBHOOK_MODE_ENV}, final: {WEBHOOK_MODE}")
logger.info(f"APP_HOST: {APP_HOST}, APP_PORT: {APP_PORT}")
logger.info(f"WEBHOOK_PATH: {WEBHOOK_PATH}")
logger.info(f"RENDER_EXTERNAL_URL: {os.getenv('RENDER_EXTERNAL_URL', 'not set')}")

def get_webhook_base_url() -> str:
    webhook_url = (WEBHOOK_URL or "").strip()
    if webhook_url:
        return webhook_url.rstrip("/")
    render_external_url = (os.getenv("RENDER_EXTERNAL_URL", "") or "").strip()
    if render_external_url:
        return render_external_url.rstrip("/")
    return ""

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
    # В режиме polling всегда удаляем вебхук, чтобы бот мог получать обновления
    # В режиме webhook удаляем только если установлен флаг DELETE_WEBHOOK_ON_STARTUP
    if not WEBHOOK_MODE or DELETE_WEBHOOK_ON_STARTUP:
        await delete_webhook(bot)
    
    # Затем устанавливаем новый вебхук, если нужно
    webhook_base_url = get_webhook_base_url()
    if WEBHOOK_MODE and webhook_base_url:
        webhook_full_url = f"{webhook_base_url}{WEBHOOK_PATH}"
        await bot.set_webhook(url=webhook_full_url)
        logger.info(f"Webhook set to {webhook_full_url}")

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
    dp.include_router(cart_router)

    # Регистрируем обработчики запуска и остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Запускаем бота в нужном режиме
    if WEBHOOK_MODE:
        # Настройка веб-сервера для вебхука
        app = web.Application()
        
        # Add health check route FIRST (before webhook handler)
        async def health_check(request):
            return web.Response(text="Bot is running!")
        app.router.add_get("/", health_check)
        
        # Настройка обработчика вебхуков
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        
        # Настройка веб-приложения
        setup_application(app, dp, bot=bot)
        
        # Запуск веб-сервера
        logger.info(f"Starting webhook server on {APP_HOST}:{APP_PORT}")
        logger.info(f"Webhook URL will be: {get_webhook_base_url()}{WEBHOOK_PATH}")
        try:
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, APP_HOST, APP_PORT)
            await site.start()
            logger.info(f"Webhook server started successfully on {APP_HOST}:{APP_PORT}")
            # Держим сервер запущенным
            try:
                await asyncio.Future()  # Бесконечное ожидание
            except asyncio.CancelledError:
                logger.info("Server shutdown requested")
            finally:
                await runner.cleanup()
        except Exception as e:
            logger.error(f"Error starting webhook: {e}")
            raise
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
