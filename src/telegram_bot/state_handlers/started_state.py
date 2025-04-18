from telegram_bot.state_handlers.base_handler import BaseStateHandler
from telegram_bot.state_handlers.end_state import EndStateHandler

from state_machine import State, SubStateUpdateExercise, SubStateUpdateSet

from telegram import Update
from telegram.ext import CallbackContext
class StartedStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)

        self.callbacks = {
            "/prev_exercise"     : self.prev_exercise,
            "/next_exercise"     : self.next_exercise,
            "/prev_set"          : self.prev_set,
            "/next_set"          : self.next_set,
            "/update_exercise"   : self.update_exercise,
            "/update_set"        : self.update_set
        }

        self.update_set_callbacks = {
            SubStateUpdateExercise.TYPE_EXPRESSION: self.type_expression
        }

        self.update_exercise_callbacks = {
            SubStateUpdateSet.TYPE_SET        : self.type_set,
            SubStateUpdateSet.TYPE_WHAT       : self.type_what,
            SubStateUpdateSet.TYPE_NEW_VALUE  : self.type_new_value
        }

        self.next_state = EndStateHandler(bot=None)

        self.resting = False # TODO: Implement the "resting state"

    async def handle_message(self, update: Update, context: CallbackContext):
        """
        Handles the message based on the substates
        and the provided command.
        ."""

        self.update = update
        self.context = context

        message = update.message

        substate_update_set = self.bot.state_machine.get_substate_update_set()
        substate_update_exercise = self.bot.state_machine.get_substate_update_exercise()

        if substate_update_set != SubStateUpdateSet.NONE:
            self.update_set_callbacks.get(substate_update_set, super().default_handler)(message=message.text)
            return

        if substate_update_exercise != SubStateUpdateExercise.NONE:
            self.update_exercise_callbacks.get(substate_update_exercise, super().default_handler)(message=message.text)
            return
        
        command = message.text.split()[0]
        
        self.callbacks.get(command, super().default_handler)(message=message.text)

    def prev_exercise(self, message):
        """
        Handles the /prev_exercise command.
        """
        # TODO
        pass

    def next_exercise(self, message):
        """
        Handles the /next_exercise command.
        """
        # TODO
        pass

    def prev_set(self, message):
        """
        Handles the /prev_set command.
        """
        # TODO
        pass

    def next_set(self, message):
        # TODO: Implement the markup when the last exercise is finished
        """
        Handls the /next_set command.
        """
        # TODO
    
    def update_set(self, message):
        """
        Handles the /update_set command.
        """
        # TODO
        pass

    def update_exercise(self, message):
        """
        Handles the /update_exercise command.
        """
        # TODO
        pass

    def type_expression(self, message): 
        """
        Handles the type_expression exercise substate.
        """
        # TODO
        pass

    def type_set(self, message):
        """
        Handles the type_set set substate.
        """
        # TODO
        pass

    def type_what(self, message):
        """
        Handles the type_what set substate.
        """
        # TODO
        pass

    def type_new_value(self, message):
        """
        Handles the type_new_value set substate.
        """
        # TODO
        pass