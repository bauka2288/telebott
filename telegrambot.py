import telebot
from telebot import types
import const
from geopy.distance import vincenty

bot = telebot.TeleBot(const.API_TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_napisat = types.KeyboardButton ('Басшыға жазу')
btn_address = types.KeyboardButton ('Соттың орналасқан жері', request_location=True)
btn_spisok = types.KeyboardButton ('Соттар тізімі')
markup_menu.add(btn_napisat, btn_address, btn_spisok)


@bot.message_handler(commands=['start', help])
def send_welcome(message):
	bot.reply_to(message, "Сәлеметсізбе? Мен көмекші ботпын", reply_markup=markup_menu)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Басшыға жазу' :
         bot.reply_to(message, 'Басшыға жазу',
                      reply_markup=markup_menu)
    elif message.text == 'Соттар тізімі' :
         bot.reply_to(message, 'Соттар тізімі',
                      reply_markup=markup_menu)
    else:
	     bot.reply_to(message, message.text, reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True, content_types=['location'])
def magazin_location(message):
    lon = message.location.longitude
    lat = message.location.latitude

    distance = []
    for m in const.MAGAZINS:
        result = vincenty((m['latm'],m['lonm']), (lat, lon)).kilometers
        distance.append(result)
    index = distance.index(min(distance))

    bot.send_message(message.chat.id, 'Шымкент қалалық соты')
    bot.send_venue(message.chat.id,
                   const.MAGAZINS[index]['latm'],
                   const.MAGAZINS[index]['lonm'],
                   const.MAGAZINS[index]['title'],
                   const.MAGAZINS[index]['address'],)


bot.polling()