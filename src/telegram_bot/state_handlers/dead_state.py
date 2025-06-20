from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.state_handlers.base_handler import BaseStateHandler
from state_machine import State, SubStateLogin

from utils import get_reply_markup

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

        self.next_state = super().get_next_state()

    def to_string(self):
        return "dead"

    async def handle_message(self, update: Update, context: CallbackContext):
        # Get message
        self.update = update
        self.context = context

        command = update.message.text.split()[0]

        await self.callbacks.get(command, super().default_handler)()

    # Callbacks
    async def start(self):
        """
        Handles /start command and shows a reply keyboard.
        """
        self.bot.state_machine[self.update.message.chat.id].set_state(State.LOGIN)
        self.bot.state_machine[self.update.message.chat.id].set_substate_login(SubStateLogin.NONE)

        self.bot.add_user(
            user_id=self.update.message.chat.id,
            chat_id=self.update.message.chat.id,
            username=self.update.message.from_user.username,
            first_name=self.update.message.from_user.first_name
        )

        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Welcome! Please enter your username to register."
        )

    async def help(self):
        """
        Handles /help command
        """

        if not self.bot.is_user_registered(self.update.message.chat.id):
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return

        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="TODO"
        )
    
    async def authenticate(self):
        """
        Handles /auth command
        """
        
        if not self.bot.is_user_registered(self.update.message.chat.id):
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return

        self.bot.state_machine[self.update.message.chat.id].set_state(State.LOGIN)
        self.bot.state_machine[self.update.message.chat.id].set_substate_login(SubStateLogin.NONE)
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Please enter your username"
        )

    async def commands(self):
        """
        Handles /commands command
        """

        if not self.bot.is_user_registered(self.update.message.chat.id):
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are not registered. Please use /start to register."
            )
            return
        
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Here are the available commands:\n\n- /help\n- /auth\n- /commands\n- /settings",
            markup_keyboard=get_reply_markup(self.next_state)
        )
    
    async def settings(self):
        """
        Handles /settings command
        """

        if not self.bot.is_user_registered(self.update.message.chat.id):
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