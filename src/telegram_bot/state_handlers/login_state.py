from telegram_bot.state_handlers.base_handler import BaseStateHandler
from telegram import Update
from telegram.ext import CallbackContext

from state_machine import State, SubStateLogin

from utils import get_reply_markup

class LoginStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.login_callbacks = {
            SubStateLogin.NONE: self.get_username,
            SubStateLogin.USERNAME: self.get_password
        }
                
        self.id = None
        self.username = None
        self.password = None

        self.max_retries = 3
        self.retries = 0

        self.next_state = super().get_next_state()
        # self.bot.state_graph.get_next_state(self.to_string())
    
    def to_string(self):
        return "login"

    async def handle_message(self, update: Update, context: CallbackContext):
        
        self.update = update
        self.context = context

        message = update.message
        
        await self.login_callbacks.get(self.bot.state_machine[message.chat.id].get_substate_login(), super().default_handler)()

    async def get_username(self):
        """
        Handles the username input
        """

        # The message received is the username
        self.username = self.update.message.text

        if self.bot.check_username(self.username):
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Valid username. Please enter your password."
            )
            self.bot.state_machine[self.update.message.chat.id].set_substate_login(SubStateLogin.USERNAME) # Username present
            return
        else:
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Username not existing. Please enter a valid username."
            )
            self.bot.state_machine[self.update.message.chat.id].set_substate_login(SubStateLogin.NONE)
            self.username = None
            return
    
    async def get_password(self):
        """
        Handles the password input
        """

        self.password = self.update.message.text

        self.id = self.bot.check_user(self.username, self.password)
        if self.id is not None:
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Valid password. You are now logged in."
            )
            self.bot.state_machine[self.update.message.chat.id].set_substate_login(SubStateLogin.PASSWORD)
            await self.authenticate()
            return
        else:
            self.retries += 1
            if self.retries >= self.max_retries:
                await self.bot.send_message(
                    chat_id=self.update.message.chat.id,
                    text="Too many attempts. Please try again later."
                )
                self.bot.remove_user(
                    user_id=self.update.message.chat.id
                )
                self.bot.state_machine[self.update.message.chat.id].set_substate_login(SubStateLogin.NONE)
                return
            else:
                await self.bot.send_message(
                    chat_id=self.update.message.chat.id,
                    text="Invalid password. Please try again. ({} attempts left)".format(self.max_retries - self.retries)
                )
                self.bot.state_machine[self.update.message.chat.id].set_substate_login(SubStateLogin.USERNAME)
                return
        
    async def authenticate(self):
        """
        Completes the authentication process.
        """
        
        self.bot.state_machine[self.update.message.chat.id].set_state(State.AUTHENTICATED)
        self.bot.state_machine[self.update.message.chat.id].set_substate_login(SubStateLogin.AUTHENTICATED)
        self.bot.id_users[self.update.message.chat.id] = self.id # Maps chat_id to user_id (from DB)
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="You are now authenticated."
        )
        
        keyboard = [['/program', '/list'],['/stats', '/help']]
        markup = self.bot.create_reply_markup(keyboard=keyboard)
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Type a command",
            markup=markup
        )