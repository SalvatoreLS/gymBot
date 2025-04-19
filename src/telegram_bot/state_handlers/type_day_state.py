from telegram_bot.state_handlers.base_handler import BaseStateHandler

from telegram import Update
from telegram.ext import CallbackContext

class TypeDayStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)


    def to_string(self):
        return "type_day"

    async def handle_message(self, update: Update, context: CallbackContext):
        
        self.update = update
        self.context = context

        message = self.update.message

        if self.bot.check_day(chat_id=self.update.message.chat.id,
                            day_id=message.text):
            self.bot.set_selected_day_id(day_id=message.text)
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Day correctly set. Workout ready to be started",
                markup=super(self.next_state, self).get_reply_markup()
            )
        else:
            self.bot.clear_program()
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Wrong day specified. Operation aborted."
            )