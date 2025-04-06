from base_handler import BaseHandler

from state_handlers.authenticated_state import AuthenticatedStateHandler

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
        # TODO
        pass

    def stats(self, message):
        """
        Handles the /stats command.
        """
        # TODO
        pass

    def suggestions(self, message):
        """
        Handles the /suggestins command.
        """
        # TODO
        pass