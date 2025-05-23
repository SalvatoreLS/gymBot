from telegram_bot.state_handlers.base_handler import BaseStateHandler

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

        self.resting = False # TODO: Implement the "resting state"

    def to_string(self):
        return "started"

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
            await self.update_set_callbacks.get(substate_update_set, super().default_handler)(message=message.text)
            return

        if substate_update_exercise != SubStateUpdateExercise.NONE:
            await self.update_exercise_callbacks.get(substate_update_exercise, super().default_handler)(message=message.text)
            return
        
        command = message.text.split()[0]
        
        await self.callbacks.get(command, super().default_handler)()

    async def prev_exercise(self):
        """
        Handles the /prev_exercise command.
        """
        # TODO
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Previous exercise - TODO"
        )

    async def next_exercise(self):
        """
        Handles the /next_exercise command.
        """
        # TODO
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Next exercise - TODO"
        )

    async def prev_set(self):
        """
        Handles the /prev_set command.
        """
        # TODO
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Previous set - TODO"
        )

    async def next_set(self):
        # TODO: Implement the markup when the last exercise is finished
        """
        Handls the /next_set command.
        """
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Next set - TODO"
        )
    
    async def update_set(self):
        """
        Handles the /update_set command.
        """
        # TODO
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Update set - TODO"
        )

    async def update_exercise(self):
        """
        Handles the /update_exercise command.
        """
        # TODO
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Update exercise - TODO"
        )

    async def type_expression(self): 
        """
        Handles the type_expression exercise substate.
        """
        # TODO
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Type expression - TODO"
        )

    async def type_set(self):
        """
        Handles the type_set set substate.
        """
        # TODO
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Type set - TODO"
        )

    async def type_what(self):
        """
        Handles the type_what set substate.
        """
        # TODO
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Type what - TODO"
        )

    async def type_new_value(self):
        """
        Handles the type_new_value set substate.
        """
        # TODO
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Type new value - TODO"
        )