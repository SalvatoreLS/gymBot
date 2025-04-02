from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your bot token
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message with inline keyboard options"""
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1')],
        [InlineKeyboardButton("Option 2", callback_data='2')],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

async def button_click(update: Update, context: CallbackContext) -> None:
    """Handles button clicks"""
    query = update.callback_query
    await query.answer()

    responses = {
        "1": "You selected Option 1!",
        "2": "You selected Option 2!",
        "3": "You selected Option 3!"
    }

    await query.edit_message_text(text=responses.get(query.data, "Invalid choice."))

def main():
    """Main function to run the bot"""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
