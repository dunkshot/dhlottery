import traceback

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import seleniumController
import telegramSender
import loadConfig
import logging

token = loadConfig.telegram_token

bot = telegram.Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()


def handler(update, context):
    try:
        user_input = update.message.text.replace(' ', '')
        logging.info('input: ' + user_input)
        telegramSender.send(user_input + ' 처리할게요. 😉')
        if user_input == '예치금충전':
            seleniumController.payment('5000')  # 5000 원
        elif user_input == '예치금조회':
            seleniumController.check_charge()
        elif user_input == '구매':
            seleniumController.buy()
        elif user_input == '결과':
            seleniumController.check_result()
        else:
            telegramSender.send('못알아듣겠어요^^🤖')
    except Exception as e:
        logging.error(traceback.format_exc())
        telegramSender.send('😵에러발생\n' + str(e))


def cron_buy():
    seleniumController.buy()


if __name__ == '__main__':
    try:
        # start logger
        logging.basicConfig(filename='dhlottery.log', format='%(asctime)s %(levelname)7s %(message)s', level=logging.INFO)

        # start buy scheduler
        sched = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 1})
        sched.add_job(cron_buy, 'cron', day='1st fri, 2nd fri, 3rd fri, last fri', hour=19, id="job1")
        sched.start()
        logging.info('[dhlottery] Start BackgroundScheduler')

        # start telegram message handler
        echo_handler = MessageHandler(Filters.text, handler)
        dispatcher.add_handler(echo_handler)
        logging.info('[dhlottery] Start msgHandler')

    except Exception as e:
        logging.error(traceback.format_exc())
        telegramSender.send('😭에러발생\n' + str(e))
