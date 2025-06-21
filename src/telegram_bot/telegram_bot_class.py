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
        self.resting_users = {}  # Maps the chat_id with the resting state of the user
        self.exercise_num_set = {}  # Maps the chat_id with a tuple (exercise_num, set_num)

    async def send_message(self, chat_id, text, markup=None):
        """
        Sends a message to the user
        """
        await self.app.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    def add_user(self, user_id: int, chat_id: int, username: str, first_name: str) -> None:
        """
        Adds a user to the database
        """
        self.user_db[user_id] = {
            "chat_id": chat_id,
            "username": username,
            "first_name": first_name
        }
        self.resting_users[user_id] = False        # Initialize resting state
        self.exercise_num_set[user_id] = (-1, -1)  # Initialize exercise and set numbers

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
        user_id = update.message.chat.id

        if user_id not in self.state_machine:
            # Initialize the state machine for the user
            self.state_machine[user_id] = StateMachine()

        # Get the user's state from the state machine
        user_state = self.state_machine[update.message.chat.id].get_state()

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

    def set_selected_program(self, program, chat_id=None):
        """
        Sets the selected program ID
        """
        self.selected_program[chat_id] = program

    def get_selected_program(self, chat_id=None) -> str:
        """
        Returns the selected program ID
        """
        return self.selected_program[chat_id].to_string()

    def clear_program(self, chat_id=None):
        """
        Sets program to none.
        """
        self.selected_program[chat_id] = None
        self.selected_day_id[chat_id] = None
    
    def set_selected_day_id(self, day_id: int, chat_id=None):
        """
        Sets the selected day ID
        """
        if chat_id is None:
            raise ValueError("chat_id must be not None")
        day_id = day_id - 1
        self.selected_day_id[chat_id] = day_id

    def get_selected_day_id(self, chat_id=None) -> int:
        """
        Returns the selected day ID
        """
        return self.selected_day_id[chat_id]
    
    def check_and_set_program(self, chat_id, program_id):
        """
        Checks if the program is valid and sets it
        """
        try:
            program_id = int(program_id)
        except ValueError:
            return False
        if self.database.check_program(self.id_users[chat_id], int(program_id)):
            self.selected_program[chat_id] = self.database.get_selected_program(self.id_users[chat_id], int(program_id))
            print("Program valid")
            return True
        return False
            
    
    def check_day(self, chat_id, day_id: str) -> bool:
        """
        Checks if the day specified is in the selected program.
        """
        try:
            day_id = int(day_id) - 1
        except ValueError:
            return False
        
        if self.selected_program is not None:
            return len(self.selected_program[chat_id].days) > day_id and day_id >= 0
        return False

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
    
    def set_user_workout_started(self, chat_id) -> bool:
        """
        Sets the user workout started state.
        """
        if chat_id not in self.resting_users or chat_id not in self.exercise_num_set:
            return False
        
        self.resting_users[chat_id] = False
        self.exercise_num_set[chat_id] = (0, 0)
        return True
    
    def get_next_exercise(self, chat_id) -> str:
        """
        Returns the next exercise for the user.
        """
        if chat_id not in self.selected_program.keys() or chat_id not in self.selected_day_id.keys():
            return "No program or day selected."
        
        program = self.selected_program[chat_id]
        day_id = self.selected_day_id[chat_id]
        exercise_num, set_num = self.exercise_num_set[chat_id]

        return """
        Exercise {}/{}: {}
        """.format(
            exercise_num + 1,
            len(program.days[day_id].exercises),
            program.days[day_id].exercises[exercise_num].to_string()
        )
    
    def increment_exercise_index(self, chat_id):
        """
        Increments the exercise index for the user.
        """
        self.exercise_num_set[chat_id] = (
            self.exercise_num_set[chat_id][0] + 1,
            self.exercise_num_set[chat_id][1]
        )

    def increment_set_index(self, chat_id):
        """
        Increments the set index for the user.
        """
        self.exercise_num_set[chat_id] = (
            self.exercise_num_set[chat_id][0],
            self.exercise_num_set[chat_id][1] + 1
        )

    def get_set_number(self, chat_id) -> int:
        """
        Returns the number of sets for the current exercise.
        """
        if chat_id not in self.selected_program.keys() or chat_id not in self.selected_day_id.keys():
            return 0
        
        program = self.selected_program[chat_id]
        day_id = self.selected_day_id[chat_id]
        exercise_num, set_num = self.exercise_num_set[chat_id]

        if exercise_num < len(program.days[day_id].exercises):
            return program.days[day_id].exercises[exercise_num].get_num_sets()
        
        return 0