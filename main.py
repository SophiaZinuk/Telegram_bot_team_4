import telebot
from telebot import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Ініціалізація телеграм-бота
bot = telebot.TeleBot('5909009806:AAG5IZowvIkUkeBAIjNd7sRr9WDtwsor6Lo')

# Підключення до Google Sheets
def get_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)
    return client

# Отримання таблиці "Номери мешканців"
def get_residents_sheet():
    client = get_google_sheets()
    sheet = client.open('Security Chatbot').worksheet('Номери мешканців')
    return sheet

# Отримання таблиці "Авто на пропуск"
def get_passes_sheet():
    client = get_google_sheets()
    sheet = client.open('Security Chatbot').worksheet('Авто на пропуск')
    return sheet

# Отримання таблиці "Оплати"
def get_payments_sheet():
    client = get_google_sheets()
    sheet = client.open('Security Chatbot').worksheet('Оплати')
    return sheet

# Отримання номерів телефонів мешканців з різних стовпців
def get_resident_phone_numbers():
    sheet = get_residents_sheet()
    residents = sheet.get_all_values()[1:]
    phone_numbers = [row[1:5] for row in residents]
    return phone_numbers

# Перевірка, чи користувач є зареєстрованим мешканцем
def is_registered_resident(user_id):
    phone_numbers = get_resident_phone_numbers()
    return any(user_id in row for row in phone_numbers)
    
# Перевірка, чи користувач зареєстрований
    if is_registered_resident(user_id):
        bot.send_message(user_id, 'Вітаємо з поверненням! Оберіть доступну опцію:', reply_markup=create_main_menu_keyboard())
    else: 
        bot.send_message(user_id, 'Ви не зареєстрований мешканець. Будь ласка, надайте свій номер телефону для реєстрації.')
        bot.register_next_step_handler(message, register_resident)

# Реєстрація мешканця
def register_resident(message):
    user_id = message.chat.id
    phone_number =message.text
    
    # Отримання номерів телефонів мешканців
    phone_numbers = get_resident_phone_numbers()
    
    # Перевірка, чи номер телефону вже існує у таблиці
    if any(phone_number in row  for row in phone_numbers):
        bot.send_message(user_id, 'Цей номер телефону вже зареєстрований.')
    else:
        # Додавання нового рядка з номером телефону
        sheet = get_residents_sheet()
        row = [user_id, phone_number]
        sheet.append_row(row)
        bot.send_message(user_id, 'Ви успішно зареєстровані як мешканець!')


# Функція для відображення головного меню
def create_main_menu_keyboard():
    # Створення клавіатури з кнопками
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Створити заявку', callback_data='new_request')
    button2 = types.InlineKeyboardButton('Стан заявок', callback_data='request_status')
    button3 = types.InlineKeyboardButton('Контакти охорони', callback_data='contacts')
    keyboard.add(button1, button2, button3)
    return keyboard

# Функція для створення клавіатури типів заявок
def create_request_type_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Taкci', callback_data='taxi')
    button2 = types.InlineKeyboardButton('Кур\'єр', callback_data='courier')
    button3 = types.InlineKeyboardButton('Гості', callback_data='guests')
    button4 = types.InlineKeyboardButton('Проблеми з парковкою', callback_data='parking')
    button5 = types.InlineKeyboardButton('Інше', callback_data='other')
    keyboard.add(button1, button2, button3, button4, button5)
    return keyboard

# Обробка команди /start
@bot.message_handler(commands=['start', 'Розпочати'])
def handle_start(message):
    user_id = message.chat.id
    # Вітальне повідомлення
    bot.send_message(user_id, '''Привіт! Я — бот охоронної служби. Я допоможу вам створити заявку 
для пропуску кур\'єра/таксі/гостей або повідомити про інші проблеми.Оберіть доступну опцію:''', reply_markup=create_main_menu_keyboard())

# Обробка натискання кнопок головного меню та підменю типів заявок
@bot.callback_query_handler(func=lambda call: True)
def handle_main_menu_buttons(call):
    user_id = call.from_user.id
    
    if call.data == 'new_request':
        bot.send_message(user_id, 'Оберіть тип заявки:', reply_markup=create_request_type_keyboard())
    elif call.data == 'request_status':
        # Обробка стану заявок
        pass
    elif call.data == 'contacts':
        # Обробка контактів охорони
        pass
    elif call.data in ['taxi', 'courier', 'guests', 'parking', 'other']:
        handler_request_type(call.data, user_id)
        

# Обробка вибраного типу заявки
def handler_request_type(request_type, user_id):
    # Додаткові дії, які необхідно виконати для кожного типу заявки
    if request_type == 'taxi':
        bot.send_message(user_id, 'Введіть номер автомобіля таксі:')
        bot.send_message(user_id, 'Оберіть КПП:', reply_markup=create_kpp_keyboard())
    elif request_type == 'courier':
        bot.send_message(user_id, 'Введіть номер автомобіля кур\'єра (опціонально):')
        bot.send_message(user_id, 'Оберіть КПП:', reply_markup=create_kpp_keyboard())
    elif request_type == 'guests':
        bot.send_message(user_id, 'Оберіть тип гостей:', reply_markup=create_guests_keyboard )
    elif request_type == 'parking':
        bot.send_message(user_id, 'Оберіть тип проблеми з парковкою:', reply_markup=create_parking_keyboard())
    else:
        bot.send_message(user_id, 'Введіть додаткові деталі про вашу заявку:')
        bot.send_message(user_id, 'Можете прикріпити фото:', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Надішліть геопозицію:', reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[
            types.KeyboardButton(text="Відправити геопозицію", request_location=True)
        ]]))
        bot.send_message(user_id, 'Надішліть файл про оплату:', reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[
            types.KeyboardButton(text="Відправити файл")
        ]]))

# Функція для створення клавіатури варіантів КПП
def create_kpp_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Перший КПП-головний', callback_data='kpp_main')
    button2 = types.InlineKeyboardButton('Другий КПП-боковий', callback_data='kpp_side')
    button3 = types.InlineKeyboardButton('Невідомо', callback_data='kpp_unknown')
    keyboard.add(button1, button2, button3)
    return keyboard

# Функція для створення клавіатури типу гостей
def create_guests_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Гості з авто', callback_data='guests_with_car')
    button2 = types.InlineKeyboardButton('Гості без авто', callback_data='guests_without_car')
    keyboard.add(button1, button2)
    return keyboard

# Функція для вибору типу гостей
@bot.callback_query_handler(func=lambda call: call.data.startswith('guest_'))
def handle_guests_type(call):
    user_id = call.message.chat.id
    guests_type = call.data.split('_')[1]
    
    if guests_type == 'with':
        bot.send_message(user_id, 'Введіть номер автомобіля гостя:')
        keyboard = create_kpp_keyboard()
        bot.send_message(user_id, 'Оберіть КПП:', reply_markup=keyboard)
    else:
        bot.send_message(user_id, 'Введіть додаткові деталі про вашу заявку:')


# Функція для створення клавіатури типу проблеми із парковкою
def create_parking_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Автомобіль заблокований', callback_data='parking_blocked')
    button2 = types.InlineKeyboardButton('Автомобіль стоїть в недозволеному місці', callback_data='parking_illegal')
    keyboard.add(button1, button2)
    return keyboard

# Обробка вибраного типу проблеми із парковкою
@bot.callback_query_handler(func=lambda call: call.data.startswith('parking_'))
def handle_parking_type(call):
    user_id = call.massage.chat.id
    parking_type = call.data.split('_')[1]
    
    bot.send_message(user_id, 'Введіть номер автомобіля порушника:')
    bot.send_message(user_id, 'Можете прикріпити фото порушення:', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(user_id, 'Можете надіслати геопозицію порушення:', reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[
        types.KeyboardButton(text="Відправити геопозицію", request_location=True)
    ]]))
    

# Функція для обробки команди /new_request або кліку на кнопку "Нова заявка"
@bot.message_handler(commands=['new_request', 'Нова заявка'])
def handle_new_request(message):
    user_id = message.chat.id
    if message.contact is not None and message.contact.phone_number is not None:
        phone_number = message.contact.phone_number
        # Пошук мешканця за номером телефону
        resident = get_resident_data(phone_number)
        if resident is not None:
            # Отримання даних про мешканця
            resident_id = resident['id']
            resident_address = get_resident_address(resident_id)

            # Перевірка стану оплати та боргу
            payment_status, debt = check_payment_status(resident_id)
            if payment_status == 'OK' or debt <= 240:
                # Додавання заявки в таблицю "Авто на пропуск"
                request_data = [resident_id, message.from_user.first_name, message.from_user.last,
                                message.from_user.username, resident_address]
                add_request_to_spreadsheet(request_data)
                # Відправка повідомлення з підтвердженням
                bot.send_message(user_id, f'Ваша заявка успішно прийнята за адресою {resident_address}.')
            elif debt > 240:
                # Відправка повідомлення про неможливість створення заявки
                bot.send_message(user_id, 'Створення заявки неможливе через наявний борг.')
        else:
            # Відправка повідомлення про невідомого користувача
            bot.send_message(user_id, 'Ви не зареєстровані як мешканець.')
    else:
        # Відправка повідомлення про відсутність контактної інформації
        bot.send_message(user_id, 'Ваша контактна інформація не надана. Будь ласка, надайте її для подальшого опрацювання.')


# Запуск бота    
if __name__ == '__main__':
    bot.infinity_polling()
    