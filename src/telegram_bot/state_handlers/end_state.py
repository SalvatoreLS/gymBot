from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.state_handlers.base_handler import BaseStateHandler

from state_machine import State

class EndStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)

        self.callbacks = {
            "/quit"         : self.quit,
            "/stats"        : self.stats,
            "/suggestions"  : self.suggestions
        }

        self.next_state = super().get_next_state()

    def to_string(self):
        return "end"
    
    async def handle_message(self, update: Update, context: CallbackContext):
        
        self.update = update
        self.context = context

        message = update.message

        command = message.text.split()[0]

        await self.callbacks.get(command, super().default_handler)(message=message)
    
    async def quit(self, message):
        """
        Handles the /quit command.
        """
        self.bot.state_machine[message.chat.id].set_state(State.AUTHENTICATED)
        await self.bot.send_message(
            chat_id=message.chat.id,
            text="Exited workout"
        )

    async def stats(self, message):
        """
        Handles the /stats command.
        """
        # TODO
        await self.bot.send_message(
            chat_id=message.chat.id,
            text="Not yet implemented - TODO"
        )

    async def suggestions(self, message):
        """
        Handles the /suggestins command.
        """
        # TODO
        await self.bot.send_message(
            chat_id=message.chat.id,
            text="Not yet implemented - TODO"
        )