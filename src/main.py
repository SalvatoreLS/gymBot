from telegram_bot.telegram_bot_class import TelegramBot

import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    tele_bot = TelegramBot(
        bot_token=os.getenv("BOT_TOKEN"),
        db_host=os.getenv("DB_HOST"),
        db_name=os.getenv("DB_NAME"),
        db_user=os.getenv("DB_USER"),
        db_password=os.getenv("DB_PASSWORD"),
        db_port=os.getenv("DB_PORT")
    )

    tele_bot.run()


if __name__ == "__main__":
    main()
