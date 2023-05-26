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


# Обробка команди /start
@bot.message_handler(commands=['start', 'Розпочати'])
def handle_start(message):
    user_id = message.chat.id
    # Відправка повідомлення зі списком операцій
    bot.send_message(user_id, '''Привіт! Я — бот охоронної служби. Я допоможу вам створити заявку 
для пропуску кур\'єра/таксі/гостей або повідомити про інші проблеми. Оберіть доступну опцію:''', reply_markup=create_main_menu_keyboard())


# Функція для відображення головного меню
def create_main_menu_keyboard():
    # Створення клавіатури з кнопками
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Створити заявку', callback_data='new_request')
    button2 = types.InlineKeyboardButton('Стан заявок', callback_data='request_status')
    button3 = types.InlineKeyboardButton('Контакти охорони', callback_data='contacts')
    keyboard.add(button1, button2, button3)
    return keyboard


# Обробка кліку на кнопку "Нова заявка"
@bot.callback_query_handler(func=lambda call: call.data == 'new_request')
def handle_new_request_click(call):
    message = call.message
    handle_new_request(message)
    
 
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

     
# Обробка вибору типу заявки
@bot.message_handler(func=lambda message:message.text in ['Таксі', 'Кур’єр', 'Гості', 'Проблеми з парковкою', 'Інше'])
def handler_request_type(message):
    user_id = message.chat.id
    request_type = message.text
    # Відправка повідомлення з підтвердженням заявки
    bot.send_message(user_id, f'Ваша заявка "{request_type}" прийнята. Очікуйте виконання.')


# Запуск бота    
if __name__ == '__main__':
    bot.infinity_polling()
    