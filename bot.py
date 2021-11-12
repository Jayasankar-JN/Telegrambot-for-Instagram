import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, commandhandler
import os
from decouple import config
from instaloader import Instaloader, Profile
import time


'''Coded by Jayasankar'''
L = Instaloader()

TOKEN = os.getenv('BOT_TOKEN')
APP_NAME = os.getenv('APP_NAME')
TELEGRAM_USERNAME = os.getenv("TELEGRAM_USERNAME")

welcome_msg = '''<b>Welcome To the Bot</b>🖐🖐
 <i>Enter the Instagram username to get their DP</i>'''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def acc_type(val):
    if(val):
        return "Private"
    else:
        return "Public"

# Start the Bot


def start(update, context):
    id = update.message.chat_id
    name = update.message.from_user['username']
    update.message.reply_html(welcome_msg)



def contact(update, context):
    keyboard = [[InlineKeyboardButton(
        "Contact", url=f"telegram.me/{TELEGRAM_USERNAME}")], ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Contact The Maker:', reply_markup=reply_markup)
    
# get the username and send the DP




def username(update, context):
    msg = update.message.reply_text("Downloading...")
    query = update.message.text
    chat_id = update.message.chat_id
    try:
        user = Profile.from_username(L.context, query)
        caption_msg = f'''*Name*: {user.full_name} \n*Followers*: {user.followers} \n*Following*: {user.followees}\
         \n*Account Type*: {acc_type(user.is_private)} \n\nCreated by : Jayasankar\nThank You For Using The bot 😀'''
        context.bot.send_photo(
            chat_id=chat_id, photo=user.profile_pic_url,
            caption=caption_msg, parse_mode='MARKDOWN')
        msg.edit_text("Found the User")
        time.sleep(5)
    except Exception:
        msg.edit_text("Try again 😕😕 Check the username correctly")



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater(TOKEN, use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(MessageHandler(Filters.text, username))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot using either webhook or polling depending on the usage
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN,webhook_url=os.getenv('WEBHOOK-URL') + TOKEN)
    #updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
