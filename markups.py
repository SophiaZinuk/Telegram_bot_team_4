import telebot
from telebot import types

'''
def board_registration():
    buttons=('Реєстрація', 'Cancel')
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    return markup.add(*[types.KeyboardButton(i) for i in buttons])
    
'''

def keyboard_registration():
    buttons=('Реєстрація', 'Cancel')
    answers=('rg_yes', 'rg_no')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup

def keyboard_request():
    buttons=('Створити заявку','Стан заявки','Контакти охорони')
    answers=('rq_create','rq_state','rq_security')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup


def keyboard_target():
    buttons=('Таксі','Кур’єр','Гості', 'Проблеми з парковкою','Інше')
    answers=('trg_taxi','trg_curier','trg_guests', 'trg_parking_problem','trg_other')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup