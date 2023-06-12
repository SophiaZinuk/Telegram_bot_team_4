import telebot
from telebot import types

def keyboard_registration():
    buttons=('Реєстрація', 'Cancel')
    answers=('rg_yes', 'rg_no')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup

def keyboard_request():
    buttons=('Нова заявка','Стан заявки','Контакти охорони')
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

def keyboard_curier():
    buttons=('Кур’єр без авто','Кур’єр з авто')
    answers=('curier_no','curier_yes')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup

def keyboard_guests():
    buttons=('Гості без авто','Гості з авто')
    answers=('guests_no','guests_yes')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup

def keyboard_problem_parking():
    buttons=('Ваш авто заблокований','Авто в недозволеному місці')
    answers=('auto_blocked','auto_incorrect_place')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup

def keyboard_select_kpp():
    buttons=('Перший КПП','Другий КПП','Невідомий')
    answers=('kpp_first','kpp_second', 'kpp_undef')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup

def keyboard_additional_info():
    buttons=('Так',' Ні')
    answers=('info_yes','info_no')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup

def sec_keyboard_get_requests():
    buttons=('Заявки','Виконати заявку')
    answers=('sec_start_rqsts','sec_start_exec')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup

def sec_keyboard_exec_rqst():
    buttons=('Виконано','Відхилено')
    answers=('sec_exec','sec_cancel')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup

def sec_keyboard_comment_answer():
    buttons=('Так',' Ні')
    answers=('sec_yes','sec_no')
    markup=types.InlineKeyboardMarkup()    
    markup.add(*[types.InlineKeyboardButton(text=buttons[i], callback_data=answers[i]) for i in range(len(buttons))])
    return markup