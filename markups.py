import telebot
from telebot import types

REGISTRATION={'rg_yes': 'Реєстрація', 'rg_no': 'Cancel'}
REQUEST={'rq_create':'Нова заявка', 'rq_state':'Стан заявки', 'rq_security':'Контакти охорони', 'rq_all_requests':'Мої заявки'}
TARGET={'trg_taxi':'Таксі', 'trg_curier':'Кур’єр', 'trg_guests':'Гості', 'trg_parking_problem':'Проблеми з парковкою', 'trg_other':'Інше'}

CURIER={'curier_no':'Кур’єр без авто', 'curier_yes':'Кур’єр з авто'}
GUESTS={'guests_no':'Гості без авто', 'guests_yes':'Гості з авто'}
PARKING={'auto_blocked':'Ваш авто заблокований', 'auto_incorrect_place':'Авто в недозволеному місці'}
INFO={'info_yes':'Так', 'info_no':'Ні'}

KPP={'kpp_first':'Перший КПП', 'kpp_second':'Другий КПП', 'kpp_undef':'Невідомий'}

SECURITY_MENU={'sec_start_rqsts':'Заявки','sec_start_exec':'Виконати заявку'}

SECURITY_EXEC_MENU={'sec_exec':'Виконано','sec_cancel':'Відхилено'}



def keyboard(buttons:dict):
    markup=types.InlineKeyboardMarkup() 
    markup.add(*[types.InlineKeyboardButton(text=button, callback_data=answer) for answer, button in buttons.items()])
    return markup

