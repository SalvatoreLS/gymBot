from state_machine import State

from telegram_bot.state_handlers.type_day_state import TypeDayStateHandler
from telegram_bot.state_handlers.base_handler import BaseStateHandler

from telegram import Update
from telegram.ext import CallbackContext

class TypeProgramStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)

        self.next_state = TypeDayStateHandler(bot=None)

    async def handle_message(self, update: Update, context):

        self.update = update
        self.context = context

        message = update.message

        if self.bot.check_and_set_program(chat_id=self.update.message.chat.id,
                                program_id=message.text):
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Selected program: " + self.bot.get_selected_program(chat_id=self.update.message.chat.id)
            )
        else:
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Program not valid. Operation aborted"
            )
            self.bot.state_machine.set_state(State.AUTHENTICATED)