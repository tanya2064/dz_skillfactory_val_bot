import telebot
from config import TOKEN, keys
from utils import ValuteConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def work_start_help(message: telebot.types.Message):
    text = ('Чтобы начать работу, введите команду в таком формате:\n'
            '<имя валюты> <в какую валюту перевести> <количество>\n'
            'Пример: доллар рубль 1\n'
            'Для списка доступных валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n' + '\n'.join(keys.keys())
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def handle_conversion(message: telebot.types.Message):
    value = message.text.lower().split(' ')

    if len(value) != 3:
        bot.send_message(message.chat.id, 'Ошибка! Введите команду в формате: <валюта1> <валюта2> <сумма>')
        return

    quote, base, amount = value
    result = ValuteConverter.convert(quote, base, amount)
    bot.send_message(message.chat.id, result)

bot.polling()