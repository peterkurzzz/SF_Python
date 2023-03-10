"""
    Решение задания 23.6.1.
    ТелеграмБОТ "Jorik".
    Используется с файлами:
     conf_23_6_1.py - конфигурационные данные
     extensions.py - классы - обработчики ошибок

"""
import telebot

from conf_23_6_1 import money, TOKEN
from extensions import CurrencyConverter, APIException


#   Создание объекта - bot
bot = telebot.TeleBot(TOKEN)


#   Обработчик команд start и help
@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты цену которой он хочет узнать>' \
           '<имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>\nУвидеть список всех ' \
           'доступных валют: /values'
    bot.reply_to(message, text)


#   Обработчик команды values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in money.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


#   Обработчик текста конвертации валюты
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        data_conv = message.text.split(' ')

        if len(data_conv) != 3:
            raise APIException('Неверное количество параметров')

        base, quote, amount = data_conv
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {base}  - {total_base} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
