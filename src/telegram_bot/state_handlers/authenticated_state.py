from base_handler import BaseHandler
from telegram import Update
from telegram.ext import CallbackContext

from state_machine import State
class AuthenticatedStateHandler(BaseHandler):
    def __init__(self, bot):
        self.bot = bot
        self.callbacks = {
            "/program" : self.program,
            "/list" : self.list,
            "/stats" : self.stats,
            "/help" : self.help
        }

        self.update = None
        self.context = None

        self.next_state = State.TYPE_PROGRAM

    async def handle_message(self, update: Update, context: CallbackContext):
        """
        Handles the message received in the authenticated state
        """
        self.update = update
        self.context = context

        message = update.message

        # Get the command and call the corresponding function
        command = message.text.split()[0]
        self.callbacks.get(command, super().default_handler)(message=message.text)
    
    def program(self, message: str):
        """
        Handles the /program command.
        User asks for a program and later types the program name
        """
        
        self.display_programs()

        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Please type the program you want to start"
        )

        self.bot.state_machine.set_state(State.TYPE_PROGRAM)

    def stats(self, message: str):
        """
        Handles the /stats command.
        User asks for the stats of a program
        """
        # TODO: Implement the stats handler and the class for getting data
        #        and visualizing the data
        
        # TODO: After shpw the markyp for commands
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Statistics finished",
            markup_keyboard=super().get_markup_keyboard()
        )


    def display_programs(self):
        """
        Displays the programs available for the user
        """

        programs_str = self.bot.get_programs(
            chat_id=self.update.message.chat.id,
        )

        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Here are the available programs:\n" + programs_str
        )
    
    def list(self, message: str):
        """
        Handles the /list command.
        User asks for the list of programs
        """
        # TODO: Retrieve the list of programs from the database
        #       it is more detailed than just the name and id

    def help(self, message: str):
        """
        Handles the /help command.
        User asks for help
        """
        # TODO: Implement the help handler
        pass