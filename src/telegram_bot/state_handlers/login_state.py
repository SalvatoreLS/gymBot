from base_handler import BaseStateHandler
from state_handlers.authenticated_state import AuthenticatedStateHandler
from telegram import Update
from telegram.ext import CallbackContext

from state_machine import State, SubStateLogin

class LoginStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.login_callbacks = {
            SubStateLogin.NONE: self.get_username,
            SubStateLogin.USERNAME: self.get_password
            # TODO: Check if the PASSWORD state requires a handler
        }
        
        self.next_state = AuthenticatedStateHandler(bot=None)
        
        self.id = None
        self.username = None
        self.password = None

        self.max_retries = 3
        self.retries = 0

    async def handle_message(self, update: Update, context: CallbackContext):
        
        self.update = update
        self.context = context

        message = update.message
        
        self.login_callbacks.get(self.bot.state_machine.get_substate_login(), super().default_handler)(message=message)

    def get_username(self, message: str):
        """
        Handles the username input
        """

        # The message received is the username
        self.username = message.text

        if self.bot.db.check_username(self.username):
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Valid username. Please enter your password."
            )
            self.bot.state_machine.set_substate_login(SubStateLogin.USERNAME) # Username present
            return
        else:
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Username not existing. Please enter a valid username."
            )
            self.bot.state_machine.set_substate_login(SubStateLogin.NONE)
            self.username = None
            return
    
    def get_password(self, message: str):
        """
        Handles the password input
        """

        self.password = message.text

        self.id = self.bot.check_user(self.username, self.password)
        if self.id is not None:
            self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Valid password. You are now logged in."
            )
            self.bot.state_machine.set_substate_login(SubStateLogin.PASSWORD)
            self.authenticate()
            return
        else:
            self.retries += 1
            if self.retries >= self.max_retries:
                self.bot.send_message(
                    chat_id=self.update.message.chat.id,
                    text="Too many attempts. Please try again later."
                )
                self.bot.remove_user(
                    user_id=self.update.message.from_user.id
                )
                self.bot.state_machine.set_substate_login(SubStateLogin.NONE)
                return
            else:

                self.bot.send_message(
                    chat_id=self.update.message.chat.id,
                    text="Invalid password. Please try again. ({} attempts left)".format(self.max_retries - self.retries)
                )
                self.bot.state_machine.set_substate_login(SubStateLogin.USERNAME)
                return
        
    def authenticate(self):
        """
        Completes the authentication process.
        """
        
        self.bot.state_machine.set_state(State.AUTHENTICATED)
        self.bot.state_machine.set_substate_login(SubStateLogin.AUTHENTICATED)
        self.bot.id_users[self.update.message.from_user.id] = self.id # Maps chat_id to user_id (from DB)
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="You are now authenticated."
        )
        # Show the menu for the next state
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Type a command",
            markup=super(self.next_state, self).get_reply_markup()
        )