from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message with a reply keyboard"""
    keyboard = [
        ["Help", "Commands"],
        ["Settings", "About"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Choose an option or type something:", reply_markup=reply_markup)

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Respond based on user input"""
    text = update.message.text.lower()
    
    responses = {
        "help": "Here is how I can help you...",
        "commands": "Available commands: /start, /help, /settings",
        "settings": "Here are your settings options...",
        "about": "I'm a Telegram bot created to assist you!"
    }

    response = responses.get(text, "I didn't understand that. Try selecting an option.")
    await update.message.reply_text(response)

def main():
    """Main function to run the bot"""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
