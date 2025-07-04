from telegram import Update
from telegram.ext import CallbackContext

from utils import get_reply_markup

from state_machine import State
from telegram_bot.state_handlers.base_handler import BaseStateHandler
class AuthenticatedStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.callbacks = {
            "/program" : self.program,
            "/list"    : self.list,
            "/stats"   : self.stats,
            "/help"    : self.help
        }

        self.next_state = super().get_next_state()
        
    
    def to_string(self):
        return "authenticated"

    async def handle_message(self, update: Update, context: CallbackContext):
        """
        Handles the message received in the authenticated state
        """
        self.update = update
        self.context = context

        message = update.message
        command = message.text.split()[0]

        await self.callbacks.get(command, super().default_handler)(message=message)
    
    async def program(self, message):
        """
        Handles the /program command.
        User asks for a program and later types the program name
        """
        
        await self.display_programs()

        await self.bot.send_message(
            chat_id=message.chat.id,
            text="Please type the program you want to start"
        )

        self.bot.state_machine[message.chat.id].set_state(State.TYPE_PROGRAM)

    async def stats(self, message):
        """
        Handles the /stats command.
        User asks for the stats of a program
        """
        # TODO: Implement the stats handler and the class for getting data
        #        and visualizing the data
        
        await self.bot.send_message(
            chat_id=message.chat.id,
            text="Statistics finished",
            markup_keyboard=get_reply_markup(self.next_state)
        )

    async def display_programs(self):
        """
        Displays the programs available for the user
        """

        programs_str = self.bot.get_string_programs(
            chat_id=self.update.message.chat.id
        )

        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Here are the available programs:\n" + programs_str
        )
    
    async def list(self, message):
        """
        Handles the /list command.
        User asks for the list of programs
        """
        programs_str = self.bot.get_programs_details(
            chat_id=message.chat.id
        )

        await self.bot.send_message(
            chat_id=message.chat.id,
            text="Here are the details about programs:\n" + programs_str
        )

    async def help(self, message):
        """
        Handles the /help command.
        User asks for help
        """
        await self.bot.send_message(
            chat_id=message.chat.id,
            text="TODO"
        )