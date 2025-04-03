from telegram import Upbdate
from telegram.ext import CallbackContext

class BaseStateHandler:
    def __init__(self, bot):
        self.bot = bot
    # TODO: Continue implementing the base state handler