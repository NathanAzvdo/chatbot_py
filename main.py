import os
from dotenv import load_dotenv
from bot.botTelegram import TelegramBot

load_dotenv()

bot_key = os.getenv("TELEGRAM_BOT_TOKEN")

if __name__ == "__main__":
    if not bot_key:
        raise ValueError("Telegram bot token não encontrado no arquivo .env")
    telegram_bot = TelegramBot(bot_key)
    telegram_bot.start()
