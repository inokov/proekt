from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, CallbackQueryHandler, filters

class AdminPhotoHandler:
    def __init__(self, bot_token, admin_id):
        self.bot_token = bot_token
        self.admin_id = admin_id
        self.application = None  # Will be assigned in the main script
        self.admin_action = None  # Variable to store admin action (confirm or reject)

    async def photo_handler(self, update: Update, context):
        # Handle the user's photo and send it to the admin with buttons
        photo = update.message.photo[-1].file_id  # Get the highest resolution photo
        buttons = [
            [
                InlineKeyboardButton("Confirm", callback_data=f"confirm_{update.message.from_user.id}"),
                InlineKeyboardButton("Reject", callback_data=f"reject_{update.message.from_user.id}")
            ]
        ]
        keyboard = InlineKeyboardMarkup(buttons)

        await context.bot.send_photo(chat_id=self.admin_id, photo=photo, caption="Photo received, confirm or reject:",
                                     reply_markup=keyboard)

    async def handle_callback(self, update: Update, context):
        # Handle the admin's decision (confirm or reject)
        query = update.callback_query
        action, user_id = query.data.split("_")

        # Store the admin's action for output
        self.admin_action = action

        if action == "confirm":
            message = "Your photo has been confirmed!"
        else:
            message = "Your photo has been rejected."

        # Send message to the user based on admin's action
        await context.bot.send_message(chat_id=user_id, text=message)

        # Send a message back to the admin and acknowledge the query
        await query.answer(f"You have {action}ed the photo.")

    def get_admin_action(self):
        # Return the latest admin action (confirm/reject)
        return self.admin_action

    def setup_application(self, application):
        # Assign the application and set up handlers
        self.application = application
        self.application.add_handler(MessageHandler(filters.PHOTO, self.photo_handler))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))