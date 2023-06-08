import telebot
from telebot import types
import google_sheets 
import markups
import handlers


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


@bot.callback_query_handler(func=lambda call: call.data in ('rq_create','rq_state','rq_security'))
def request(call):
    if call.data=='rq_security':
        bot.answer_callback_query(call.id, 'Good')
        bot.send_message(call.message.chat.id, text=google_sheets.security_contact())
    elif call.data=='rq_create':
        bot.answer_callback_query(call.id, 'Ok')
        bot.send_message(call.message.chat.id, text='Оберіть мету заявки:', reply_markup=markups.keyboard_target())
    
    elif call.data=='rq_state':
        #!!!!check request and send request_state
        return


def create_rq(user_avto): #!!!!!!redone
    rqst={'id_request': google_sheets.get_id_rqst(), #number of previos id+1
           'id_user': user_avto.from_user.id, 
           'adress': google_sheets.get_adress(user_avto.from_user.id), 
           'telephone': google_sheets.get_telephone(user_avto.from_user.id),
           'target':rqst[0],
           'num_avto': rqst[1], 
           'message': rqst[2], #??
           'date': user_avto.date,
           'status': 0
           }
    
    rqst_text=str([str(i)+': '+str(j) for i,j in rqst.items()])
    return rqst_text


def add_number_avto(id_user):
    #rqst.append(id_user.text)
    mes=bot.send_message(id_user.chat.id, text='Введіть additioanal info')
    bot.register_next_step_handler(mes, add_message)

def add_message(id_user):    
    #rqst.append(id_user.text)
    info='create_rq(id_user)'
    bot.send_message(id_user.chat.id, text=info)

@bot.callback_query_handler(func=lambda call: call.data in ('trg_taxi','trg_curier','trg_guests', 'trg_parking_problem','trg_other'))
def target(call):
    if call.data=='trg_taxi':
        
        bot.answer_callback_query(call.id, 'Ok')
        avto=bot.send_message(call.message.chat.id, text='Введіть номер авто')
                        
        bot.register_next_step_handler(avto, add_number_avto) #!!next input message
       

    elif call.data=='trg_curier':
        pass
    elif call.data=='trg_guests':
        pass
    elif call.data=='trg_parking_problem':
        pass
    elif call.data=='trg_other':
        pass
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
