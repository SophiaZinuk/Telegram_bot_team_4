import telebot
from telebot import types
import google_sheets 
import markups
import handlers


TOKEN_BOT='6093636754:AAEXctCKEmEVM-nhms6g7ss8t7huY4wRPq0'

bot=telebot.TeleBot(TOKEN_BOT)

## ['id_request', 'id_user', 'adress', 'telephone', 'target', 'number of avto', 'additional info', 'kpp', 'date', 'status']
HEAD_RQST_SHEET=google_sheets.get_head()
dict_rqst=dict()




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
def handler_registration(call):
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
def requests(call):
    if call.data=='rq_security':
        bot.answer_callback_query(call.id, 'Good')
        bot.send_message(call.message.chat.id, text=google_sheets.security_contact())
        return
    elif call.data=='rq_create':
        dict_rqst=dict()
        bot.answer_callback_query(call.id, 'Ok')
        bot.send_message(call.message.chat.id, text='Оберіть мету заявки:', reply_markup=markups.keyboard_target())
        return
    elif call.data=='rq_state':        
        #input number of requsest
        number=bot.send_message(call.message.chat.id, text='Введіть номер заявки')
        bot.register_next_step_handler(number, get_status_request)
        return

#!!???
def add_to_new_request(mes, New_request: list):
    return New_request.append(mes)       

def get_status_request(number):
    if number.text.strip().isdigit():
        text=google_sheets.get_state_request(id_user=number.from_user.id, id_request=int(number.text))
    else:
        text='Введено некорректні дані!'
    bot.send_message(number.from_user.id, text=f'Статус заявки № {number.text} "{text}"')


@bot.callback_query_handler(func=lambda call: call.data in ('trg_taxi','trg_curier','trg_guests', 'trg_parking_problem','trg_other'))
def handler_target(call):
    ## ['id_request', 'id_user', 'adress', 'telephone', 'target', 'number of avto', 'additional info', 'kpp', 'date', 'status']
    dict_rqst['id_request']=google_sheets.get_id_rqst()
    dict_rqst['id_user']=call.message.chat.id
    dict_rqst['adress']= google_sheets.get_adress(call.message.chat.id)
    dict_rqst['telephone']=google_sheets.get_telephone(call.message.chat.id)
    dict_rqst['date']=call.message.date
    dict_rqst['status']=0

    if call.data=='trg_taxi':
        dict_rqst['target']='Таксі'
        bot.answer_callback_query(call.id, 'Ok')
        num_auto=bot.send_message(call.message.chat.id, text='Введіть номер авто')  
                      
        bot.register_next_step_handler(num_auto, add_num_auto) # next input message
            

    elif call.data=='trg_curier':        
        bot.send_message(call.message.chat.id, text='Виберіть опцію для кур`єра', reply_markup=markups.keyboard_curier())
        
    
    elif call.data=='trg_guests':        
        bot.send_message(call.message.chat.id, text='Виберіть опцію для Гості', reply_markup=markups.keyboard_guests())
        
    elif call.data=='trg_parking_problem':
        
        bot.send_message(call.message.chat.id, text='Виберіть опцію для Проблеми з парковкою', reply_markup=markups.keyboard_problem_parking())
    
    elif call.data=='trg_other':
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['target']='Інше'
        dict_rqst['number of avto']=None                 
        
        info=bot.send_message(call.message.chat.id, text='Введіть інформацію:')
        bot.register_next_step_handler(info, add_kpp) 


def add_num_auto(message): 
    dict_rqst['number of avto']=message.text
    bot.send_message(message.chat.id, text='Бажаєте ввести додаткову інформацію?', reply_markup=markups.keyboard_additional_info()) 
  

@bot.callback_query_handler(func=lambda call: call.data in ('info_yes','info_no'))
def handler_target(call):
    if call.data=='info_yes':
        info=bot.send_message(call.message.chat.id, text='Введіть додаткову інформацію')
        bot.register_next_step_handler(info, add_kpp)
    elif call.data=='info_no':
        dict_rqst['additional info']=''
        bot.send_message(call.message.chat.id, text='Оберіть КПП:', reply_markup=markups.keyboard_select_kpp())


def add_kpp(id_user):
    dict_rqst['additional info']=id_user.text
    bot.send_message(id_user.chat.id, text='Оберіть КПП:', reply_markup=markups.keyboard_select_kpp())    
    

@bot.callback_query_handler(func=lambda call: call.data in ('kpp_first','kpp_second', 'kpp_undef'))
def handler_kpp(call): 
    if call.data=='kpp_first':
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['kpp']='first kpp'
    elif call.data=='kpp_second':
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['kpp']='second kpp'
    elif call.data=='kpp_undef':
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['kpp']='undefined kpp'
    
    mes=bot.send_message(call.message.chat.id, text='Ваша заявка напрвлена в обробку')
    create_rq(mes)
    #bot.register_next_step_handler(mes, create_rq)   ##!!!!!!!
#!!!!!!!!!!!!

@bot.callback_query_handler(func=lambda call: call.data in ('curier_no','curier_yes'))
def handler_curier(call):       
    if call.data=='curier_no':
        bot.answer_callback_query(call.id, 'Good') 

        dict_rqst['target']='Кур’єр без авто'              
        dict_rqst['number of avto']=None
        info=bot.send_message(call.message.chat.id, text='Введіть інформацію про кур’єра:')
        bot.register_next_step_handler(info, add_kpp)

    elif call.data=='curier_yes':
        bot.answer_callback_query(call.id, 'Ok')
        dict_rqst['target']='Кур’єр з авто'         
        num_auto=bot.send_message(call.message.chat.id, text='Введіть номер авто')                       
        bot.register_next_step_handler(num_auto, add_num_auto) # next input message


@bot.callback_query_handler(func=lambda call: call.data in ('guests_no','guests_yes'))
def handler_guests(call):      
    if call.data=='guests_no':
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['target']='Гості без авто'  
        dict_rqst['number of avto']=None
        info=bot.send_message(call.message.chat.id, text='Введіть інформацію щодо гостей:')
        bot.register_next_step_handler(info, add_kpp)

    elif call.data=='guests_yes':
        bot.answer_callback_query(call.id, 'Ok')
        dict_rqst['target']='Гості з авто'
        num_auto=bot.send_message(call.message.chat.id, text='Введіть номер авто')                       
        bot.register_next_step_handler(num_auto, add_num_auto) # next input message 


@bot.callback_query_handler(func=lambda call: call.data in ('auto_blocked','auto_incorrect_place'))
def handler_parking(call): 
    target='Проблеми з парковкою.'     
    if call.data=='auto_blocked':
        target+=' Ваш авто заблокований' 
    elif call.data=='auto_incorrect_place':
        target+=' Авто в недозволеному місці'

    bot.answer_callback_query(call.id, 'Ok')
    dict_rqst['target']=target
    num_auto=bot.send_message(call.message.chat.id, text='Введіть номер авто')                       
    bot.register_next_step_handler(num_auto, add_num_auto) # next input message 




def create_rq(message): #  !!!! redo add KPP
    request=[]
    for i in HEAD_RQST_SHEET:
        request.append(dict_rqst[i]) if i in dict_rqst.keys() else request.append(None)    
    google_sheets.add_request(request)    
    bot.send_message(message.chat.id, text=f'Ваша заявка № {request[0]} прийнята!')


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
