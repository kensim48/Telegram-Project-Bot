import random

API_TOKEN = "970240642:AAGe-LkIAGQTe_gky5lAKB9IUKKv57nJyC4"

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

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

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import _thread
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
quote_text1 = open("quotes1.txt", "r")
quote_list1 = quote_text1.read().split('\n')
quote_text1.close()
quote_text2 = open("quotes2.txt", "r")
quote_list2 = quote_text2.read().split('\n')
quote_text2.close()
callout_text = open("callouts.txt", "r")
callout_list = [x.lower() for x in callout_text.read().split('\n')]
callout_text.close()
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Help!')


def all_messages_logger(message):
    f = open("logs/{}_logs.txt".format(message.chat['title']), "a+")
    f.write("{}\t{}\n".format(message.from_user, message.text))
    f.close()
    print("{}:\t{}:\t{}\n".format(message.chat['title'], message.from_user["first_name"], message.text))

def all_messages(bot, update):
    """Echo the user message."""
    _thread.start_new_thread(all_messages_logger, (update.message,))
    for check_text in callout_list:
        if check_text in update.message.text.lower():
            buzzword = ""
            reply = ""
            for i in range(1, random.randrange(4)):
                buzzword += quote_list1[random.randrange(len(quote_list1))] + " "
            reply = buzzword + quote_list2[random.randrange(len(quote_list2))]
            reply = reply.replace("<?$NAME?>", update.message.from_user["first_name"])
            bot.send_message(chat_id=update.message.chat_id, text=reply)
            print("Called")
            break

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(API_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, all_messages))

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