import telebot
from telebot import types

bot=telebot.TeleBot('6093636754:AAEXctCKEmEVM-nhms6g7ss8t7huY4wRPq0')

@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    # bt1 = types.KeyboardButton(text = 'Я - житель')
    # bt2 = types.KeyboardButton(text = 'Я - охоронець')
    bt1 = types.InlineKeyboardButton(text = 'Я - житель', callback_data='bt1')
    bt2 = types.InlineKeyboardButton(text = 'Я - охоронець' , callback_data='bt2')
    kb.add(bt1, bt2)
    mes=f'Hello, {message.from_user.first_name}'
    bot.send_message(message.chat.id, message.chat.id, reply_markup=kb)

# @bot.callback_query_handler(func = lambda callback: callback.data)
# def check_callback_start_data(callback):
#     if callback.data == 'bt1':
#         kb = types.InlineKeyboardMarkup()
#         bt1 = types.InlineKeyboardButton(text = 'Реєстрація')
#         bt2 = types.InlineKeyboardButton(text='Вийти')
#         kb.add(bt1, bt2)
#         bot.send_message(chat_id=callback.message.chat.id ,text = 'Вітаю, жителю!', reply_markup=kb)
#     elif callback.data == 'bt2':
#         bot.send_message(callback.message.chat.id, 'Вітаю, охоронцю')

# @bot.message_handler(commands=['guardian'])
# def guardian(message):
#     kb = types.InlineKeyboardMarkup()
#     bt1 = types.InlineKeyboardButton(text='Введіть пароль', callback_data='password')
#     bt2 = types.InlineKeyboardButton(text='Вийти')
#     kb.add(bt1, bt2)
#     mes = 'Привіт, виберіть опцію'
#     bot.send_message(message.chat.id, mes, reply_markup=kb)

bot.polling()