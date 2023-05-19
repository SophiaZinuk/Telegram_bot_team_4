import telebot
from telebot import types

# Ініціалізуємо телеграм-бота
bot = telebot.TeleBot('5909009806:AAG5IZowvIkUkeBAIjNd7sRr9WDtwsor6Lo')

# Обробка команди /start
@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привіт, я бот охоронної служби. Я допоможу вам створити заявку для пропуску кур\'єра/таксі/гостей або повідомити про інші проблеми. Щоб ознайомитися з усіма моїми можливостями, введіть команду /help.')

# Обробка команди /help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Цей бот допоможе вам створити заявку для охорони. Доступні наступні команди:\n/start - почати спілкування з ботом\n/help - допомога...')

# Обробка команди /new_request
@bot.message_handler(commands=['new_request'])
def handle_new_request(message):
    # Створення клавіатури з кнопками
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Takci')
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
    