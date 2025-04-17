from telegram import Update
from telegram.ext import CallbackContext
from base_handler import BaseHandler
from state_handlers.login_state import LoginStateHandler
from state_machine import State, SubStateLogin

class DeadStateHandler(BaseHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.callbacks = {
            "/start"    : self.start,
            "/help"     : self.help,
            "/auth"     : self.authenticate,
            "/commands" : self.commands,
            "/settings" : self.settings
        }
        self.next_state = LoginStateHandler(bot=None)

    async def handle_message(self, update: Update, context: CallbackContext):
        # Get message
        self.update = update
        self.context = context

        message = update.message

        command = message.text.split()[0]

        self.callbacks.get(command, super().default_handler)(message=command)

    # Callbacks
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

    def help(self, message: str):
        """
        Handles /help command
        """

        if not self.bot.is_user_registered(self.update.message.from_user.id):
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return

        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="TODO"
        )
    
    def authenticate(self, message: str):
        """
        Handles /auth command
        """
        
        if not self.bot.is_user_registered(self.update.message.from_user.id):
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return

        self.bot.state_machine.set_state(State.LOGIN)
        self.bot.state_machine.set_substate_login(SubStateLogin.NONE)
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Please enter your username"
        )

    def commands(self, message: str):
        """
        Handles /commands command
        """

        if not self.bot.is_user_registered(self.update.message.from_user.id):
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return
        
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Here are the available commands:\n\n- /help\n- /auth\n- /commands\n- /settings",
            markup_keyboard=super().get_markup_keyboard()
        )
    
    def settings(self, message: str):
        """
        Handles /settings command
        """

        if not self.bot.is_user_registered(self.update.message.from_user.id):
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return
        
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Here are the available settings:\n\n- /help\n- /auth\n- /commands\n- /settings"
        )

        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Setting not implemented yet TODO ??"
        )