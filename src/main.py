from telegram_bot import TelegramBot
from database import Database

import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    tele_bot = TelegramBot(os.getenv("BOT_TOKEN"))

    tele_bot.run()


if __name__ == "__main__":
    main()
