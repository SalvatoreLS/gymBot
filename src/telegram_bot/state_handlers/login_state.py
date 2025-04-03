from base_handler import BaseStateHandler

class LoginStateHandler(BaseStateHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.state = "login"

    def handle_message(self, message):
        # Handle login messages
        if message.text == "/login":
            self.bot.send_message(message.chat.id, "Please enter your username and password.")
        else:
            self.bot.send_message(message.chat.id, "Invalid command. Please use /login to start the login process.")

    def handle_callback(self, callback):
        # Handle login callbacks
        if callback.data == "login_success":
            self.bot.send_message(callback.message.chat.id, "Login successful!")
        else:
            self.bot.send_message(callback.message.chat.id, "Login failed. Please try again.")