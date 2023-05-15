import telebot

# Ініціалізуємо телеграм-бота
bot = telebot.TeleBot('5909009806:AAG5IZowvIkUkeBAIjNd7sRr9WDtwsor6Lo')

# Оброблювач повідомлень для команди /start
@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привіт, я бот охоронної служби. Я допоможу вам створити заявку для пропуску кур\'єра/таксі/гостей або повідомити про інші проблеми. Щоб ознайомитися з усіма моїми можливостями, введіть команду /help.')

# Оброблювач повідомлень для команди /help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Цей бот допоможе вам створити заявку для охорони. Доступні наступні команди:\n/start - почати спілкування з ботом\n/help - допомога...')
    
if __name__ == '__main__':
    bot.polling()