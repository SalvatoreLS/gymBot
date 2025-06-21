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

    async def default_handler(self):
        """
        Default handler for all states
        """
        await self.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text="Invalid command. Please try again."
        )

    def get_next_state(self):
        """
        Returns the next state of the state machine.
        """
        return self.bot.state_graph.get_next_state(self.to_string())
    
    def get_callbacks(self):
        """
        Returns the callbacks for the state
        """
        return list(self.callbacks.keys())

    def get_reply_markup(self):
        """
        Returns the markup keyboard for the user or None.
        """

        keys = self.get_callbacks()

        if len(keys) % 2 != 0:
            keys.append("- - -")

        markup_keyboard = []

        if len(keys) == 0:
            return None

        for i in range(0, len(keys), 2):
            markup_keyboard.append(keys[i:i+2])
        return markup_keyboard