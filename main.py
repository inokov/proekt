from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from python import AdminPhotoHandler

# Replace with your bot token and admin's chat ID
BOT_TOKEN = ""
ADMIN_ID = ""

# Create an instance of the AdminPhotoHandler class
admin_handler = AdminPhotoHandler(BOT_TOKEN, ADMIN_ID)

async def start(update: Update, context):
    # Send message to the user to send a photo
    await update.message.reply_text("Hi, send me a pic.")

def main():
    # Create the Application and pass it the bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Set up the bot application handlers via the admin_handler class
    admin_handler.setup_application(application)

    # Add the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Start the bot to handle photos and admin decisions
    application.run_polling()

if __name__ == "__main__":
    main()
