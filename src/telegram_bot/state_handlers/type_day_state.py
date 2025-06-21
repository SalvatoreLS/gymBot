from telegram_bot.state_handlers.base_handler import BaseStateHandler

from telegram import Update
from telegram.ext import CallbackContext

from state_machine import State

from utils import get_reply_markup

class TypeDayStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.next_state = super().get_next_state()


    def to_string(self):
        return "type_day"

    async def handle_message(self, update: Update, context: CallbackContext):
        
        self.update = update
        self.context = context

        message = self.update.message

        keyboard = ["/start_workout", "/cancel"]
        if self.bot.check_day(chat_id=message.chat.id,
                            day_id=message.text):
            self.bot.set_selected_day_id(day_id=int(message.text.strip()), chat_id=message.chat.id)
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Day correctly set. Workout ready to be started",
                markup=self.bot.create_reply_markup(keyboard=[keyboard])
            )
            self.bot.state_machine[message.chat.id].set_state(State.READY)

        else:
            self.bot.clear_program()
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Wrong day specified. Operation aborted."
            )