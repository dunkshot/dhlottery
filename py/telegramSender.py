"""
Done! Congratulations on your new bot. You will find it at t.me/DhlotteryBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
5260793847:AAHQBZljoUiNTHAJ-y1orZHxO25U2KBPlKE
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
"""

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os

token = '5260793847:AAHQBZljoUiNTHAJ-y1orZHxO25U2KBPlKE'
chat_id = 370311245


def send(msg):
    print("telegram sender done. : " + msg)
    bot = telegram.Bot(token=token)
    result = bot.sendMessage(chat_id=chat_id, text=msg)
    print(result)


def send_img(img_name):
    if os.path.exists(img_name):
        bot = telegram.Bot(token=token)
        bot.send_photo(chat_id, open(img_name, 'rb'))
        os.remove(img_name)

# updater = Updater(token=token, use_context=True)
