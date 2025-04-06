from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

from database import Database
from state_machine import StateMachine
from state_machine import State

# State handlers
from telegram_bot.state_handlers.dead_state import DeadStateHandler
from telegram_bot.state_handlers.login_state import LoginStateHandler
from telegram_bot.state_handlers.authenticated_state import AuthenticatedStateHandler
from telegram_bot.state_handlers.type_program_state import TypeProgramStateHandler
from telegram_bot.state_handlers.type_day_state import TypeDayStateHandler
from telegram_bot.state_handlers.ready_state import ReadyStateHandler
from telegram_bot.state_handlers.started_state import StartedStateHandler
from telegram_bot.state_handlers.end_state import EndStateHandler

class TelegramBot:
    """
    Class handling all the operations of the bot
    """
    def __init__(self, bot_token, db_url, db_auth_key) -> None:
        self.token = bot_token
        self.app = Application.builder().token(self.token).build()
        self.state_machine = StateMachine()

        self.database = Database(
            db_url=db_url,
            db_auth_key=db_auth_key)
        
        self.user_db = {}

        self.state_handlers = {
            State.DEAD           :  DeadStateHandler(self),
            State.LOGIN          :  LoginStateHandler(self),
            State.AUTHENTICATED  :  AuthenticatedStateHandler(self),
            State.TYPE_PROGRAM   :  TypeProgramStateHandler(self),
            State.TYPE_DAY       :  TypeDayStateHandler(self),
            State.READY          :  ReadyStateHandler(self),
            State.STARTED        :  StartedStateHandler(self),
            State.END            :  EndStateHandler(self)
        }

        self.selected_program = {}
        self.selected_day_id = {}

        # Add command handlers
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(CallbackQueryHandler(self.button_click))
    
    def send_message(self, chat_id, text, markup=None):
        """
        Sends a message to the user
        """
        self.app.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    def add_user(self, user_id, chat_id, username, first_name):
        """
        Adds a user to the database
        """
        self.user_db[user_id] = {
            "chat_id": chat_id,
            "username": username,
            "first_name": first_name
        }

    def remove_user(self, user_id):
        """
        Removes a user from the database
        """
        if user_id in self.user_db:
            del self.user_db[user_id]

    def check_username(self, username: str) -> bool:
        """
        Checks if the username is already taken
        """
        # TODO: Check if the username is on the DB 
        return False

    def check_user(self, username: str, password: str) -> bool:
        """
        Checks if the user exists in the database
        """
        # TODO: Check if the user exists in the DB
        return False

    def is_user_registered(self, user_id):
        """
        Checks if a user is registered in user_db
        """
        return user_id in self.user_db

    def get_programs(self, chat_id):
        """
        Queries the database for the programs associated with the user
        """
        # TODO: Implement the logic to get the programs from the database
        # TODO: Return the program ids such that the user can select that
        pass

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
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id

        # Check if the user is in the database
        if user_id not in self.user_db:
            await update.message.reply_text("You are not registered. Please use /start to register.")
            return

        # Get the user's state from the state machine
        user_state = self.state_machine.get_state()

        # Handle the message based on the user's state
        handler = self.state_handlers.get(user_state)
        if handler:
            await handler.handle_message(update, context)

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

    def set_selected_program(self, program):
        """
        Sets the selected program ID
        """
        self.selected_program = program

    def get_selected_program(self): # TODO: check if chat_id is needed based on how the bot interacts with multiple users
        """
        Returns the selected program ID
        """
        return self.selected_program

    def clear_program(self):
        """
        Sets program to none.
        """
        self.selected_program = None
        self.selected_day_id = None
    
    def set_selected_day_id(self, day_id):
        """
        Sets the selected day ID
        """
        self.selected_day_id = day_id

    def get_selected_day_id(self):
        """
        Returns the selected day ID
        """
        return self.selected_day_id
    
    def check_and_set_program(self, chat_id, program_id):
        """
        Checks if the program is valid and sets it
        """
        # TODO: Check if the program exists in the database
        # and set it as the selected program
        pass
    
    def check_day(self, chat_id, day_id):
        """
        Checks if the day specified is in the selected program.
        """
        pass

    def run(self) -> None:
        """
        Runs the bot
        """
        print("Bot is running...")
        self.app.run_polling()