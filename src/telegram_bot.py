from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

from database import Database
from state_machine import State

class TelegramBot:
    """
    Class handling all the operations of the bot
    """
    def __init__(self, bot_token, db_url, db_auth_key) -> None:
        self.token = bot_token
        self.app = Application.builder().token(self.token).build()
        self.state = State.DEAD
        self.database = Database(
            db_url=db_url,
            db_auth_key=db_auth_key)
        self.user_db = {}

        # Add command handlers
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(CallbackQueryHandler(self.button_click))

    async def start(self, update: Update, context: CallbackContext) -> None:
        """
        Handles /start command and shows a reply keyboard.
        """
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        user_first_name = update.message.from_user.first_name

        self.user_db[user_id] = {
            "chat_id": update.message.chat.id,
            "username": username,
            "first_name": user_first_name
        }
        await update.message.reply_text(f"Hello {user_first_name}, welcome to the bot!")

        keyboard = [["/help", "/commands"], ["/settings", "/start"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

        await update.message.reply_text("Welcome to the telegram bot. Choose an option or type something", reply_markup=reply_markup)

    async def help(self, update: Update, context: CallbackContext) -> None:
        """
        Handles /help command
        """
        await update.message.reply_text("Here is how I can help you...")
        
        keyboard = [["/help", "/commands"], ["/settings", "/start"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text("Choose an option or type something", reply_markup=reply_markup)

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        """
        Handles text messages from users
        """
        text = update.message.text.lower()

        responses = {
            "help": "Here is how I can help you...",
            "commands": "Available commands: /start, /help, /settings",
            "settings": "Here are your settings options...",
            "about": "I'm a Telegram bot created to assist you!"
        }

        response = responses.get(text, "I didn't understand that. Please try again.")
        await update.message.reply_text(response)

    async def button_click(self, update: Update, context: CallbackContext) -> None:
        """
        Handles button clicks from inline keyboards
        """
        query = update.callback_query
        await query.answer()

        responses = {
            "1": "You selected Option 1!",
            "2": "You selected Option 2!",
            "3": "You selected Option 3!"
        }

        await query.edit_message_text(text=responses.get(query.data, "Invalid choice."))

    def run(self) -> None:
        """
        Runs the bot
        """
        print("Bot is running...")
        self.app.run_polling()

    # TODO: Implement all the functionalities of the bot