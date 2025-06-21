from telegram_bot.state_handlers.base_handler import BaseStateHandler
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

        self.next_state = super().get_next_state()
    
    def to_string(self):
        return "ready"
    
    async def handle_message(self, update: Update, context: CallbackContext):
        
        self.update = update
        self.context = context

        message = update.message

        command = message.text.split()[0]
        await self.callbacks.get(command, super().default_handler)()

    async def start_workout(self):
        """
        Handles the /start_workout command.
        """
        self.bot.state_machine[self.update.message.chat.id].set_state(State.STARTED)
        self.bot.state_machine[self.update.message.chat.id].set_substate_update_set(SubStateUpdateSet.NONE)
        self.bot.state_machine[self.update.message.chat.id].set_substate_update_exercise(SubStateUpdateExercise.NONE)

        if not self.bot.set_user_workout_started(chat_id=self.update.message.chat.id):
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Error starting workout. Please try again later."
            )
            return

        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Workout started!"
        )
        await self.bot.send_message(
            chat_id = self.update.message.chat.id,
            text = self.bot.get_next_exercise(chat_id = self.update.message.chat.id)
        )
        self.bot.increment_exercise_index(chat_id=self.update.message.chat.id)
    
    async def cancel(self):
        """
        Handles the /cancel command.
        """
        self.bot.state_machine.set_state(State.AUTHENTICATED)
        # TODO: Add the possibility to hold the previously selected
        # program in memory and automatically ask the user to start that
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Workout cancelled."
        )
    