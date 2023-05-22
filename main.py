import telebot
from telebot import types

# Ініціалізуємо телеграм-бота
bot = telebot.TeleBot('5909009806:AAG5IZowvIkUkeBAIjNd7sRr9WDtwsor6Lo')

# Обробка команди /start
@bot.message_handler(commands=['start', 'Розпочати'])
def handle_start(message):
    show_main_menu(message.chat.id)
    
# Функція для відображення головного меню
def show_main_menu(chat_id):
    # Створення клавіатури з кнопками
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Нова заявка')
    button2 = types.KeyboardButton('Стан заявок')
    button3 = types.KeyboardButton('Контакти')
    keyboard.add(button1, button2, button3)

    # Відправка повідомлення зі списком операцій
    bot.send_message(chat_id, '''Привіт! Я — бот охоронної служби. Я допоможу вам створити заявку 
    для пропуску кур\'єра/таксі/гостей або повідомити про інші проблеми. Оберіть доступну операцію:''', reply_markup=keyboard)

# Обробка команди /new_request
@bot.message_handler(commands=['new_request'])
def handle_new_request(message):
    # Створення клавіатури з кнопками
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Taкci')
    button2 = types.KeyboardButton('Кур’єр')
    button3 = types.KeyboardButton('Гості')
    button4 = types.KeyboardButton('Проблеми з парковкою')
    button5 = types.KeyboardButton('Інше')
    keyboard.add(button1, button2, button3, button4, button5)

    bot.send_message(message.chat.id, 'Оберіть тип заявки:', reply_markup=keyboard)
    
# Обробка вибору типу заявки
@bot.message_handler(func=lambda message:message.text in ['Таксі', 'Кур’єр', 'Гості', 'Проблеми з парковкою', 'Інше'])
def handler_request_type(message):
    request_type = message.txt
    # Обробка типу заявки і отримання необхідних даних
    # Збереження заявки в базі даних
    # Відправка підтвердження заявки
    pass

# Запуск бота    
if __name__ == '__main__':
    bot.polling()
    