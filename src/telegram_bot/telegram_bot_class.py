from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

from database import Database
from state_machine import StateMachine
from state_machine import State

from telegram_bot.state_handlers.state_graph import StateGraph

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
    def __init__(self,
                 bot_token,
                 db_host, db_password, db_user, db_name, db_port) -> None:
        self.token = bot_token
        self.app = Application.builder().token(self.token).build()
        self.state_machine = {}

        self.database = Database(
            db_host=db_host,
            db_password=db_password,
            db_user=db_user,
            db_name=db_name,
            db_port=db_port
        )
        
        self.user_db = {}   # Stores user data in memory
        self.id_users = {}  # Maps the id of the user in DB with the chat_id (chat_id : user_id)

        self.app.add_handler(MessageHandler(filters.ALL, self.handle_message))

        self.state_graph = StateGraph()

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
    
    async def send_message(self, chat_id, text, markup=None):
        """
        Sends a message to the user
        """
        await self.app.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

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
        return self.database.check_username(username=username)

    def check_user(self, username: str, password: str) -> int|None:
        """
        Checks if the user exists in the database
        """
        return self.database.check_user(username=username, password=password)

    def is_user_registered(self, user_id):
        return user_id in self.user_db

    def get_string_programs(self, chat_id) -> str:
        """Returns the available programs as a formatted string."""
        returned_string = ""
        return self.database.get_programs(self.id_users[chat_id])

    def get_programs_details(self, chat_id) -> str:
        """
        Returns a more detailed list of programs when requested by user.
        """
        return self.database.get_programs_details(self.id_users[chat_id])

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        """
        Handles text messages from users
        """
        user_id = update.message.from_user.id

        if user_id not in self.state_machine:
            # Initialize the state machine for the user
            self.state_machine[user_id] = StateMachine()

        # Get the user's state from the state machine
        user_state = self.state_machine[update.message.from_user.id].get_state()

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

    def get_selected_program(self):
        """
        Returns the selected program ID
        """
        return self.selected_program.to_string()

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
        try:
            program_id = int(program_id)
        except ValueError:
            return False
        if self.database.check_program(self.id_users[chat_id], int(program_id)):
            self.selected_program = self.database.get_selected_program(self.id_users[chat_id], int(program_id))
            print("Program valid")
            return True
        return False
            
    
    def check_day(self, chat_id, day_id):
        """
        Checks if the day specified is in the selected program.
        """
        # TODO: define a dictionary of programs and change the code before

    def run(self) -> None:
        """
        Runs the bot
        """
        print("Bot is running...")
        self.app.run_polling()

    def create_reply_markup(self, keyboard):
        return ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            resize_keyboard=True)