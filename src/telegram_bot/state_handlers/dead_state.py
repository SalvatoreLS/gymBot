from telegram import Update
from telegram.ext import CallbackContext
from base_handler import BaseHandler
from state_machine import State, SubStateLogin

class DeadStateHandler(BaseHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.callbacks = {
            "/start"    : self.start,
            "/help"     : self.help,
            "/auth"     : self.authenticate
        }
        self.update = None
        self.context = None

    async def handle_message(self, update: Update, context: CallbackContext):
        # Get message
        self.callbacks.get(update.message.text, self.default_handler)(message=update.message.text)

    
    def start(self, message: str):
        """
        Handles /start command and shows a reply keyboard.
        """
        self.bot.state_machine.set_state(State.LOGIN)
        self.bot.state_machine.set_substate_login(SubStateLogin.NONE)

        self.bot.add_user(
            user_id=self.update.message.from_user.id,
            chat_id=self.update.message.chat.id,
            username=self.update.message.from_user.username,
            first_name=self.update.message.from_user.first_name
        )

        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Hello, welcome to the bot! Please enter your username"
        )

    def help(self, message: str):
        """
        Handles /help command
        """
        # TODO: define what to say here

        if not self.bot.is_user_registered(self.update.message.from_user.id):
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return
    
    def authenticate(self, message: str):
        """
        Handles /auth command
        """
        # TODO: when user types /auth, ask for username and password and switch state