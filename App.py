import telebot
from telebot import types
from Config import TOKEN, keys
from Extensions import ConvertionExeption, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    marcup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Помощь')
    item2 = types.KeyboardButton('Список валют:')
    item3 = types.KeyboardButton('API')
    item4 = types.KeyboardButton('Информация')

    marcup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Здравствуйте, пришли посмотреть курс валют?'.format(message.from_user),
                     reply_markup=marcup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Помощь':
            bot.send_message(message.chat.id, 'Для конвертации, введите команду: '
                                              '\n[Валюта] [Валюта в которую перевести] [Сумма]')
        elif message.text == 'API':
            bot.send_message(message.chat.id, 'cryptocompare.com')

        elif message.text == 'Список валют:':
            for key in keys.keys():
                message.text = '\n'.join((message.text, key,))
            bot.send_message(message.chat.id, message.text)

        elif message.text == 'Информация':
            bot.send_message(
                message.chat.id, 'Бот для конвертации валют')
        else:
            try:
                value = message.text.split(' ')

                if len(value) != 3:
                    raise ConvertionExeption('Слишком много параметров.')

                quote, base, amount = value
                total_base = CryptoConverter.convert(quote, base, amount)

            except ConvertionExeption as e:
                bot.reply_to(message, f'Ошибка пользователя. \n{e}')

            except Exception as e:
                bot.reply_to(message, f'Не удалось обработать команду\n{e}')

            else:
                text = f'За {amount} - {quote} вы получите \n{total_base * int(amount)} - {base} ' \
                       f'\nпо курсу cryptocompare.com'
                bot.send_message(message.chat.id, text)


bot.polling()
