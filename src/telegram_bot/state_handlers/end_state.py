from base_handler import BaseHandler

class EndStateHandler(BaseHandler):
    async def handle_message(self, message):
        """
        Handle the end state of the workout.
        """
        await self.send_message(
            chat_id=message.chat.id,
            text="Workout completed! Here are your results:\n\n" + self.get_string_results(),
            reply_markup=None # TODO: define reply markup for further actions
        )
        # Optionally, you can reset the conversation state or perform any cleanup here.
        self.reset_conversation_state(message.chat.id)
    
    def get_string_results(self):
        """
        Convert the results to a string format for display.
        """