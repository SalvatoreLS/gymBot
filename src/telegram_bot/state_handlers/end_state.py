from base_handler import BaseHandler

from state_handlers.authenticated_state import AuthenticatedStateHandler

from state_machine import State

class EndStateHandler(BaseHandler):
    def __init__(self, bot):
        super().__init__(bot)

        self.callbacks = {
            "/quit"         : self.quit,
            "/stats"        : self.stats,
            "/suggestions"  : self.suggestions
        }

        self.next_state = AuthenticatedStateHandler(bot=None)
    
    async def handle_message(self, update, context):
        
        self.update = update
        self.context = context

        message = update.message

        command = message.text.split()[0]

        self.callbacks.get(command, super().default_handler)(message=message.text)
    
    def quit(self, message):
        """
        Handles the /quit command.
        """
        self.bot.state_machine.set_state(State.AUTHENTICATED)
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Exited workout"
        )

    def stats(self, message):
        """
        Handles the /stats command.
        """
        # TODO
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Not yet implemented - TODO"
        )

    def suggestions(self, message):
        """
        Handles the /suggestins command.
        """
        # TODO
        self.bot.send_message(
            chat_id=self.update.message.chat.id,
            text="Not yet implemented - TODO"
        )