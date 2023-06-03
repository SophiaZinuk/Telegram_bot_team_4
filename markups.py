import telebot
from telebot import types


def registration():
    buttons=['Реєстрація', 'cancel']
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    return markup.add(types.KeyboardButton(i) for i in buttons)
    
