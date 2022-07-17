import telegram
from datetime import datetime
import pytz
import time
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

token = '5260793847:AAHQBZljoUiNTHAJ-y1orZHxO25U2KBPlKE'
utc = pytz.UTC

# current_time = datetime.now()
current_time = datetime.utcnow()
print('now: ' + str(current_time))
# time.sleep(3)

bot = telegram.Bot(token=token)
chat_id = 370311245

# print(bot.get_chat(370311245))
a = bot.get_updates(offset=-1)
print(a[0])
for i in a:
    text = i['message']['text']
    date = i['message']['date']
    print(text + ': ' + str(date))
    # print(type(date))  # <class 'datetime.datetime'>

    # print(current_time)
    # print(type(current_time))

    # date_ = utc.localize(date)
    current_time_ = utc.localize(current_time)

    print(current_time_ > date)

# updates = bot.getUpdates()
# for i in updates:
#     print(i.message)




