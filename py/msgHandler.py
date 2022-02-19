import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import seleniumController
import telegramSender
import loadConfig

token = loadConfig.telegram_token

bot = telegram.Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()


def handler(update, context):
    try:
        user_input = update.message.text.replace(' ', '')
        print('input: ' + user_input)
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
        telegramSender.send('😵에러발생\n' + str(e))


try:
    print('Start msgHandler')
    echo_handler = MessageHandler(Filters.text, handler)
    dispatcher.add_handler(echo_handler)
except Exception as e:
    telegramSender.send('😭에러발생\n' + str(e))
