from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.state_handlers.state_graph import StateGraph

class BaseStateHandler:
    def __init__(self, bot):
        self.bot = bot
        self.next_state = None
        self.update = None
        self.context = None
        self.callbacks = {}

    def to_string(self):
        return "base"

    def default_handler(self, message: str):
        """
        Default handler for all states
        """
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Invalid command. Please try again."
        )
    
    def get_callbacks(self):
        """
        Returns the callbacks for the state
        """
        return self.callbacks.keys()

    def get_markup_keyboard(self):
        """
        Returns the markup keyboard for the user
        """

        keys = self.next_state.get_callbacks()

        markup_keyboard = []

        for i in range(0, len(keys), 2):
            markup_keyboard.append(keys[i:i+2])
        return markup_keyboard