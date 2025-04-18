from telegram_bot.telegram_bot_class import TelegramBot
from database import Database

import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    tele_bot = TelegramBot(
        bot_token=os.getenv("BOT_TOKEN"),
        db_url=os.getenv("DB_URL"),
        db_auth_key=os.getenv("DB_KEY"))

    tele_bot.run()


if __name__ == "__main__":
    main()
