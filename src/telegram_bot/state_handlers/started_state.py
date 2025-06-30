from telegram_bot.state_handlers.base_handler import BaseStateHandler

from state_machine import State, SubStateUpdateExercise, SubStateUpdateSet
from program_classes import ExerciseUpdate

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

        self.next_state = super().get_next_state()

        self.update_exercise_callbacks = {
            SubStateUpdateExercise.NONE           : self.none_exercise,
            SubStateUpdateExercise.TYPE_EXPRESSION: self.type_expression
        }

        self.update_set_callbacks = {
            SubStateUpdateSet.NONE            : self.none_state,
            SubStateUpdateSet.TYPE_SET        : self.type_set,
            SubStateUpdateSet.TYPE_WHAT       : self.type_what,
            SubStateUpdateSet.TYPE_NEW_VALUE  : self.type_new_value
        }

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
        
        substate_update_set = self.bot.state_machine[message.chat.id].get_substate_update_set()
        substate_update_exercise = self.bot.state_machine[message.chat.id].get_substate_update_exercise()

        if substate_update_set == SubStateUpdateSet.NONE and substate_update_exercise == SubStateUpdateExercise.NONE:
            await self.callbacks.get(message.text.split()[0], super().default_handler)(message=message)
        elif substate_update_set != SubStateUpdateSet.NONE:
            await self.update_set(message)
        elif substate_update_exercise != SubStateUpdateExercise.NONE:
            await self.update_exercise(message)

    async def prev_exercise(self, message):
        """
        Handles the /prev_exercise command.
        """
        exercise_num = self.bot.get_exercise_num(chat_id=message.chat.id)
        if exercise_num <= 1:
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are already at the first exercise."
            )
            return
        self.bot.decrement_exercise_index(chat_id=self.update.message.chat.id)
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text=self.bot.get_next_exercise(chat_id=self.update.message.chat.id)
        )
        await self.bot.send_message(
            chat_id=message.chat.id,
            text=f"Set {self.bot.get_set_number(chat_id=message.chat.id)} of {self.bot.get_all_sets_num(chat_id=message.chat.id, exercise_num=exercise_num)}:\n\n{self.bot.get_exercise_set(chat_id=message.chat.id)}"
        )

    async def next_exercise(self, message):
        """
        Handles the /next_exercise command.
        """
        program = self.bot.selected_program[self.update.message.chat.id]
        day_id = self.bot.selected_day_id[self.update.message.chat.id]
        total_exercises = len(program.days[day_id].exercises)
        exercise_num = self.bot.get_exercise_num(chat_id=message.chat.id)

        if exercise_num >= total_exercises:
            keyboard = [["/stats", "/suggestions"], ["-", "/quit"]]
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="Workout finished! Congratulations!",
                markup=self.bot.create_reply_markup(keyboard=keyboard)
            )
            self.bot.state_machine[self.update.message.chat.id].set_state(State.END)
            return
        
        self.bot.increment_exercise_index(chat_id=self.update.message.chat.id)
        self.bot.reset_set_index(chat_id=self.update.message.chat.id)
        
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text=self.bot.get_next_exercise(chat_id=self.update.message.chat.id)
        )
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text=f"Set {self.bot.get_set_number(chat_id=self.update.message.chat.id)} of {self.bot.get_all_sets_num(chat_id=message.chat.id, exercise_num=exercise_num)}:\n\n{self.bot.get_exercise_set(chat_id=self.update.message.chat.id)}"
        )

    async def prev_set(self, message):
        """
        Handles the /prev_set command.
        """
        if self.bot.get_set_number(chat_id=self.update.message.chat.id) <= 1:
            await self.bot.send_message(
                chat_id=self.update.message.chat.id,
                text="You are already at the first set."
            )
            return
        self.bot.decrement_set_index(chat_id=self.update.message.chat.id)
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text=self.bot.ge
        )

    async def next_set(self, message):
        """
        Handls the /next_set command.
        """
        if self.bot.get_set_number(chat_id=message.chat.id) >= self.bot.get_set_number(chat_id=message.chat.id):
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Exercise finished!"
            )
            self.bot.increment_exercise_index(chat_id=message.chat.id)
            self.bot.reset_set_index(chat_id=message.chat.id)
            if self.bot.get_exercise_num(chat_id=message.chat.id) >= self.bot.get_exercise_num(chat_id=message.chat.id):
                await self.bot.send_message(
                    chat_id=message.chat.id,
                    text="Workout finished! Congratulations!"
                )
                self.bot.state_machine[message.chat.id].set_state(State.END)
                return
            await self.bot.send_message(
                chat_id=message.chat.id,
                text=self.bot.get_next_exercise(chat_id=message.chat.id)
            )
            await self.bot.send_message(
                chat_id=message.chat.id,
                text=f"Set {self.bot.get_set_number(chat_id=message.chat.id)} of {self.bot.get_exercise_num(chat_id=message.chat.id)}:\n\n{self.bot.get_exercise_set(chat_id=message.chat.id)}"
            )
            return
        self.bot.increment_set_index(chat_id=message.chat.id)
        await self.bot.send_message(
            chat_id=message.chat.id,
            text=f"Set {self.bot.get_set_number(chat_id=message.chat.id)} of {self.bot.get_exercise_num(chat_id=message.chat.id)}:\n\n{self.bot.get_exercise_set(chat_id=message.chat.id)}"
        )
    
    async def update_set(self, message):
        """
        Handles the /update_set command.
        """
        substate_update_set = self.bot.state_machine[message.chat.id].get_substate_update_set()
        await self.update_set_callbacks.get(substate_update_set, super().default_handler)(message=message)

    async def update_exercise(self, message):
        """
        Handles the /update_exercise command.
        """
        substate_update_exercise = self.bot.state_machine[message.chat.id].get_substate_update_exercise()
        await self.update_exercise_callbacks.get(substate_update_exercise, super().default_handler)(message=message)

    async def none_exercise(self, message):
        """
        Handles the none exercise substate.
        """
        await self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Type the expression of the exercise you want to update."
        )
        self.bot.state_machine[self.update.message.chat.id].set_substate_update_exercise(SubStateUpdateExercise.TYPE_EXPRESSION)

    async def type_expression(self, message): 
        """
        Handles the type_expression exercise substate.
        """
        # TODO
        if self.bot.update_by_expression(chat_id=message.chat.id, expression=message.text.strip()):
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Exercise updated successfully."
            )
        else:
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Error updating exercise. Please try again later."
            )
        self.bot.state_machine[message.chat.id].set_substate_update_exercise(SubStateUpdateExercise.NONE)
    
    async def none_state(self, message):
        """
        Handles the none state for update set.
        """
        await self.bot.send_message(
            chat_id=message.chat.id,
            text="Type the number of the set you want to update."
        )
        self.bot.updating[message.chat.id] = ExerciseUpdate()
        exercise_num = self.bot.get_exercise_num(chat_id=message.chat.id)
        self.bot.add_to_updating(chat_id=message.chat.id, exercise_num=exercise_num)
        self.bot.state_machine[message.chat.id].set_substate_update_set(SubStateUpdateSet.TYPE_SET)

    async def type_set(self, message):
        """
        Handles the type_set set substate.
        """
        try:
            set_number = int(message.text)
        except ValueError:
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Please enter a valid set number."
            )
            return
        if set_number < 1 or set_number > self.bot.get_set_number(chat_id=message.chat.id):
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Set number out of range. Please enter a valid set number."
            )
            return
        
        exercise_num = self.bot.get_exercise_num(chat_id=message.chat.id)
        self.bot.add_to_updating(chat_id=message.chat.id, exercise_num=exercise_num, set_num=set_number)
        self.bot.state_machine[message.chat.id].set_substate_update_set(SubStateUpdateSet.TYPE_WHAT)
        await self.bot.send_message(
            chat_id=message.chat.id,
            text=f"Set {set_number} selected. What would you like to update?"
        )
        await self.bot.send_message(
            chat_id=message.chat.id,
            text="1 - Reps\n2 - Rest\n3 - Weight\n0 - Cancel",
            markup=self.bot.create_reply_markup(keyboard=[["0", "1"], ["2", "3"]])
        )

    async def type_what(self, message):
        """
        Handles the type_what set substate.
        """
        try:
            what_to_update = int(message.text)
        except ValueError:
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Please enter a valid number for what to update."
            )
            return
        if what_to_update < 0 or what_to_update > 3: # supporting only weight, rest, reps (will support more in the future)
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Invalid option. Please enter a valid number (0-3)."
            )
            return
        if what_to_update == 0:
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Update cancelled."
            )
            self.bot.state_machine[message.chat.id].set_substate_update_set(SubStateUpdateSet.NONE)
            return
        self.bot.add_to_updating(chat_id=message.chat.id, what_to_update=what_to_update)
        self.bot.state_machine[message.chat.id].set_substate_update_set(SubStateUpdateSet.TYPE_NEW_VALUE)
        await self.bot.send_message(
            chat_id=message.chat.id,
            text="Please enter the new value."
        )

    async def type_new_value(self, message):
        """
        Handles the type_new_value set substate.
        """
        try:
            new_value = int(message.text)
        except ValueError:
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Please enter a valid number for the new value."
            )
            return
        if new_value < 0:
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Negative values are not allowed. Please enter a valid number."
            )
            return
        self.bot.add_to_updating(chat_id=message.chat.id, value_to_update=new_value)
        self.bot.state_machine[message.chat.id].set_substate_update_exercise(SubStateUpdateExercise.NONE)
        if self.bot.update_exercise(chat_id=message.chat.id):
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Exercise updated successfully.",
                markup=self.bot.create_reply_markup(keyboard=[["/prev_exercise", "/next_exercise"], ["/prev_set", "/next_set"]])
            )
            self.bot.check_and_set_program(chat_id=message.chat.id, program_id=self.bot.selected_program[message.chat.id].id)
            self.bot.state_machine[message.chat.id].set_substate_update_set(SubStateUpdateSet.NONE)
            exercise_num = self.bot.get_exercise_num(chat_id=message.chat.id)
            await self.bot.send_message(
                chat_id=message.chat.id,
                text=f"Set {self.bot.get_set_number(chat_id=self.update.message.chat.id)} of {self.bot.get_all_sets_num(chat_id=message.chat.id, exercise_num=exercise_num)}:\n\n{self.bot.get_exercise_set(chat_id=self.update.message.chat.id)}"
            )
        else:
            await self.bot.send_message(
                chat_id=message.chat.id,
                text="Error updating exercise. Please try again later."
            )