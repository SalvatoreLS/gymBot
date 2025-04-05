from base_handler import BaseStateHandler

from state_machine import State

class TypeProgramStateHandler(BaseStateHandler):
    def __init__(self, bot):
        self.update = None
        self.context = None

        self.next_state = State.TYPE_DAY

    async def handle_message(self, update, context):

        self.update = update
        self.context = context

        message = update.message

        if self.bot.check_and_set_program(chat_id=self.update.message.chat.id,
                                program_id=message.text):
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Selected program: " + self.bot.get_selected_program(chat_id=self.update.message.chat.id) # TODO: Check the functioning of the telegram bot with multiple users
            )