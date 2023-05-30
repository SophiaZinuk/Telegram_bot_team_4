import telebot
from telebot import types



TOKEN_BOT='6093636754:AAEXctCKEmEVM-nhms6g7ss8t7huY4wRPq0'

bot=telebot.TeleBot(TOKEN_BOT)

#start
@bot.message_handler(commands=['start'])
def start(message):
    mes=f'Hello, {message.from_user.first_name}'
    bot.send_message(message.chat.id, mes)

'''#get text
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text.lower()=='hello':
        bot.send_message(message.chat.id, message.from_user.id)
    else:
        bot.send_message(message.chat.id, "I don't understand you")
'''

#get photo
@bot.message_handler(content_types='photo')
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Photo')

#display submits
@bot.message_handler(commands=['submit'])
def submit(message):
    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Open site', url='https://pypi.org/project/pyTelegramBotAPI/'))
    bot.send_message(message.chat.id, 'Open!', reply_markup=markup)

#help /show submits
@bot.message_handler(commands=['help'])
def submit(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    call=types.KeyboardButton('Zayavka' )
    taxi=types.KeyboardButton('Taxi')
    markup.add(call, taxi)
    bot.send_message(message.chat.id, 'Go!', reply_markup=markup)



bot.polling(non_stop=True)
