from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.state_handlers.base_handler import BaseStateHandler
from state_machine import State, SubStateLogin

class DeadStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.callbacks = {
            "/start"    : self.start,
            "/help"     : self.help,
            "/auth"     : self.authenticate,
            "/commands" : self.commands,
            "/settings" : self.settings
        }

    def to_string(self):
        return "dead"

    async def handle_message(self, update: Update, context: CallbackContext):
        # Get message
        self.update = update
        self.context = context

        command = update.message.text.split()[0]

        await self.callbacks.get(command, super().default_handler)(message=command)

    # Callbacks
    async def start(self, message: str):
        """
        Handles /start command and shows a reply keyboard.
        """
        print("Start command received by dead state handler")
        self.bot.state_machine[self.update.message.from_user.id].set_state(State.LOGIN)
        self.bot.state_machine[self.update.message.from_user.id].set_substate_login(SubStateLogin.NONE)

        self.bot.add_user(
            user_id=self.update.message.from_user.id,
            chat_id=self.update.message.chat.id,
            username=self.update.message.from_user.username,
            first_name=self.update.message.from_user.first_name
        )

        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Welcome! Please enter your username to register."
        )

    async def help(self, message: str):
        """
        Handles /help command
        """

        if not self.bot.is_user_registered(self.update.message.from_user.id):
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return

        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="TODO"
        )
    
    async def authenticate(self, message: str):
        """
        Handles /auth command
        """
        
        if not self.bot.is_user_registered(self.update.message.from_user.id):
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return

        self.bot.state_machine[self.update.message.from_user.id].set_state(State.LOGIN)
        self.bot.state_machine[self.update.message.from_user.id].set_substate_login(SubStateLogin.NONE)
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Please enter your username"
        )

    async def commands(self, message: str):
        """
        Handles /commands command
        """

        if not self.bot.is_user_registered(self.update.message.from_user.id):
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return
        
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Here are the available commands:\n\n- /help\n- /auth\n- /commands\n- /settings",
            markup_keyboard=super().get_markup_keyboard()
        )
    
    async def settings(self, message: str):
        """
        Handles /settings command
        """

        if not self.bot.is_user_registered(self.update.message.from_user.id):
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return
        
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Here are the available settings:\n\n- /help\n- /auth\n- /commands\n- /settings"
        )

        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Setting not implemented yet TODO ??"
        )