import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

@dataclass
class BotConfig:
    token: str
    admin_id: int  # Your Telegram user ID
    db_path: str = "database/bot_database.db"

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided in environment variables")

# Получаем ID администратора
ADMIN_ID = os.getenv('ADMIN_ID')
if not ADMIN_ID:
    raise ValueError("No ADMIN_ID provided in environment variables")

# Путь к базе данных
DB_PATH = os.getenv('DB_PATH', 'database/bot_database.db')

config = BotConfig(
    token=BOT_TOKEN,
    admin_id=int(ADMIN_ID),
    db_path=DB_PATH
)