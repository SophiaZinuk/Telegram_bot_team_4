import telebot
from telebot import types
import google_sheets 
import markups



TOKEN_BOT='6093636754:AAEXctCKEmEVM-nhms6g7ss8t7huY4wRPq0'

bot=telebot.TeleBot(TOKEN_BOT)


#start
@bot.message_handler(commands=['start','use'])
def start(message):
    mes=f'Привіт, {message.from_user.first_name}! Вас вітає ЖК Мрія.'
    bot.send_message(message.chat.id, mes)
    id_user=message.from_user.id
    #check in db_tenants
    if google_sheets.is_user_telegram(id_user)==False:
        #goto menu request
        bot.send_message(message.chat.id, 'З поверненням!', reply_markup=markups.keyboard_request()) 
        
    else:
        #show button 'registration', 'cancel'
        markup=markups.keyboard_registration()
        bot.send_message(message.chat.id, 'Бажаєте зареєструватись?', reply_markup=markup)
        


@bot.callback_query_handler(func=lambda call: call.data in ('rg_yes', 'rg_no'))
def registration(call):
    if call.data=='rg_yes':
        bot.answer_callback_query(call.id, 'Good')
        mes_for_tel_number='Відправте Ваш номер телефону для реєстрації у боті.'
        phone_number=bot.send_message(call.message.chat.id, text=mes_for_tel_number)
        
        bot.register_next_step_handler(phone_number, phone)
       
    else:
        bot.answer_callback_query(call.id, 'Ohhhh')
        return

@bot.callback_query_handler(func=lambda call: call.data in ('rq_create','rq_state','rq_security'))
def request(call):
    pass


def phone(number):    
    correct_number=google_sheets.is_correct_number(number.text)
    #check is correct number
    if correct_number:
        if google_sheets.is_in_db_tenants(correct_number):
            
            google_sheets.add_user_id(number.chat.id, correct_number)
            bot.send_message(number.chat.id, text='Ви успішно зареєстровані')
            bot.send_message(number.chat.id, 'Оберіть дію: ', reply_markup=markups.keyboard_request()) 

        else:
            bot.send_message(number.chat.id, text='Ваш номер телефону не знайдено! Зверніться до адміністрації')
    
    else: #is incorrect, repeat it
        repeat_number=bot.send_message(number.chat.id, text='Введіть корректний номер телефону!')
        bot.register_next_step_handler(repeat_number, phone) 




'''    

@bot.callback_query_handler(func=lambda callback: callback=callback.data)
def registration(callback):
    bot.send_message(callback.chat.id, 'URAAAAAA')

    
#get text
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text.lower()=='hello':
        bot.send_message(message.chat.id, message.from_user.id)
    else:
        bot.send_message(message.chat.id, "I don't understand you")


#get photo
@bot.message_handler(content_types='photo')
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Photo')

#display submits
@bot.message_handler(commands=['submit'])
def submit(message):
    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Open site', url='https://pypi.org/project/pyTelegramBotAPI/'))
    bot.send_message(message.chat.id, 'Open!', reply_markup=markup)

#help /show submits
@bot.message_handler(commands=['help'])
def submit(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    call=types.KeyboardButton('Zayavka' )
    taxi=types.KeyboardButton('Taxi')
    markup.add(call, taxi)
    bot.send_message(message.chat.id, 'Go!', reply_markup=markup)

'''

bot.polling(non_stop=True)
