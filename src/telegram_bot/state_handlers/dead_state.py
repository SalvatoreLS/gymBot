from telegram import Update
from telegram.ext import CallbackContext
from base_handler import BaseHandler

class DeadStateHandler(BaseHandler):
    async def handle_message(self, update: Update, context: CallbackContext):
        await update.message.reply_text("The bot is inactive. Type /start to activate it.")