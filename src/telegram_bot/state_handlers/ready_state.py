from telegram_bot.state_handlers.base_handler import BaseStateHandler
from telegram_bot.state_handlers.started_state import StartedStateHandler
from state_machine import State, SubStateUpdateSet, SubStateUpdateExercise

from telegram import Update
from telegram.ext import CallbackContext

class ReadyStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)
        
        self.callbacks = {
            "/start_workout" : self.start_workout,
            "/cancel"        : self.cancel
        }

        self.next_state = StartedStateHandler(bot=None)
    
    async def handle_message(self, update: Update, context: CallbackContext):
        
        self.update = update
        self.context = context

        message = update.message

        command = message.text.split()[0]
        self.callbacks.get(command, super().default_handler)(message=message.text)

    def start_workout(self, message):
        """
        Handles the /start_workout command.
        """
        self.bot.state_machine.set_state(State.STARTED)
        self.bot.state_machine.set_substate_update_set(SubStateUpdateSet.NONE)
        self.bot.state_machine.set_substate_update_exercise(SubStateUpdateExercise.NONE)

        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Workout started!"
        )
        # TODO: Show the first exercise from the selected day
        """
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text=...) # Get exercise from program
        """
    
    def cancel(self, message):
        """
        Handles the /cancel command.
        """
        self.bot.state_machine.set_state(State.AUTHENTICATED)
        # TODO: Add the possibility to hold the previously selected
        # program in memory and automatically ask the user to start that
    