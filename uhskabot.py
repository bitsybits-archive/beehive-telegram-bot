#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import animations
import audios
import config
import datetime
import logging
import stickers
import sys

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

logPath = 'logs'
# Log to stdout
console_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(console_handler)
# Log to file
if config.SAVE_LOGS:
    log_file_name = str(datetime.datetime.now())
    file_handler = logging.FileHandler('{0}/{1}.log'.format(logPath, log_file_name))
    logger.addHandler(file_handler)


def track_user(update, action):
    if not config.ENABLE_TRACKING:
        return

    user = update.message.from_user
    logger.info('Action %s\n\tText: %s\n\tFrom: %s %s',
        action, update.message.text, user.first_name, user.last_name)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    track_user(update, '/start')

    update.message.reply_text('Welcome to Beehive bot!\n\n'
        'Commands: /start /help and then try to find easter eggs!')

    reply_keyboard = [['Boy', 'Girl', 'Other']]
    update.message.reply_text(
        'Hi! My name is BeehiveBot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def help(update, context):
    """Send a message when the command /help is issued."""
    track_user(update, '/help')

    update.message.reply_voice(audios.NE_LEZ_SKA)


def gender(update, context):
    track_user(update, 'GENDER')

    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    if update.message.text == "Other":
        update.message.reply_sticker(stickers.MCCOUNAGHEY)
    elif update.message.text == "Boy":
        update.message.reply_animation(animations.DICAPRIO_CONGRATS)
    elif update.message.text == "Girl":
        update.message.reply_animation(animations.BOUNCING_HEAD_YES)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def text_handler(update, context):
    track_user(update, 'TEXT')
    if update.message.text.lower() == 'uh' \
       or update.message.text.lower() == 'uh ska' \
       or update.message.text.lower() == 'ууска':
        update.message.reply_sticker(stickers.UH_SKA)
        update.message.reply_voice(audios.UH_SKA)
    else:
        update.message.reply_text(update.message.text)


def sticker_handler(update, context):
    logger.info('Received sticker: %s', update.message.sticker)
    update.message.reply_text("Nice sticker!")


def animation_handler(update, context):
    logger.info('Received animation: %s', update.message.animation)
    update.message.reply_text("Nice animation!")


def audio_handler(update, context):
    logger.info('Received audio: %s', update.message.audio)
    update.message.reply_text("Nice audio!")


def voice_handler(update, context):
    logger.info('Received voice: %s', update.message.voice)
    update.message.reply_text("Nice voice!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender))
    dp.add_handler(MessageHandler(Filters.text, text_handler))

    # FOR TEST ONLY
    if config.TEST_MODE:
        dp.add_handler(MessageHandler(Filters.sticker, sticker_handler))
        dp.add_handler(MessageHandler(Filters.animation, animation_handler))
        dp.add_handler(MessageHandler(Filters.audio, audio_handler))
        dp.add_handler(MessageHandler(Filters.voice, voice_handler))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
