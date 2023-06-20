import telebot
from telebot import types
import google_sheets 
import markups
#import handlers


TOKEN_BOT='6093636754:AAEXctCKEmEVM-nhms6g7ss8t7huY4wRPq0'

bot=telebot.TeleBot(TOKEN_BOT)

## columns of request.sheet:
## ['id_request', 'id_user', 'adress', 'telephone', 'target', 'number of avto', 'additional info', 'kpp', 'date', 'status']
HEAD_RQST_SHEET=google_sheets.get_head()
dict_rqst=dict()


#start
@bot.message_handler(commands=['start','use'])
def start(message):
    mes=f'Привіт, {message.from_user.first_name}! '

    #check id on user or security
    if google_sheets.check_security(message.chat.id):
        mes+='Охорона.'
        bot.send_message(message.chat.id, mes, reply_markup=markups.keyboard(markups.SECURITY_MENU))
    
    else:

        mes+=' Вас вітає ЖК Мрія.'
        bot.send_message(message.chat.id, mes)
        id_user=message.from_user.id
        #check in db_tenants
        if google_sheets.is_user(id_user):
            #goto menu request
            bot.send_message(message.chat.id, 'З поверненням!', reply_markup=markups.keyboard(markups.REQUEST)) 
            
        else:
            #show button 'registration', 'cancel'
            bot.send_message(message.chat.id, 'Бажаєте зареєструватись?', reply_markup=markups.keyboard(markups.REGISTRATION))

            
### Security handlers
@bot.callback_query_handler(func=lambda call: call.data in markups.SECURITY_MENU.keys())
def sec_main_menu_handler(call):
    if call.data=='sec_start_rqsts':
        bot.answer_callback_query(call.id, text='Good') 
        answer=markups.SECURITY_MENU['sec_start_rqsts']

        list_requests=google_sheets.sec_get_list_requests()
        if list_requests:
            for rqst in list_requests:
                bot.send_message(call.message.chat.id, text=rqst)
        else:
            bot.send_message(call.message.chat.id, text='Ваш список пустий')
        bot.send_message(call.message.chat.id, text='Оберіть дію', reply_markup=markups.keyboard(markups.SECURITY_MENU))
        
    elif call.data=='sec_start_exec':
        bot.answer_callback_query(call.id, text='Good') 
        answer=markups.SECURITY_MENU['sec_start_exec']

        number_rqst=bot.send_message(call.message.chat.id, text='Введіть номер заявки:')
        bot.register_next_step_handler(number_rqst, sec_exec)
    
    # delete buttons 
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=None)
   

def sec_exec(message):
    id_rqst=message.text
    if id_rqst.strip().isdigit():
        
        if int(id_rqst) in google_sheets.sec_get_list_id_requests():
            bot.send_message(message.chat.id, text='Оберіть дію для заявки № ')
            bot.send_message(message.chat.id, text=id_rqst, reply_markup=markups.keyboard(markups.SECURITY_EXEC_MENU))
        else:
            bot.send_message(message.chat.id, text='Заявка виконана або не існує')
            bot.send_message(message.chat.id, text='Оберіть дію', reply_markup=markups.keyboard(markups.SECURITY_MENU))

    else:
        bot.send_message(message.chat.id, text='Введено некоректні дані')
        bot.send_message(message.chat.id, text='Оберіть дію', reply_markup=markups.keyboard(markups.SECURITY_MENU))



@bot.callback_query_handler(func=lambda call: call.data in markups.SECURITY_EXEC_MENU.keys())
def sec_main_menu_handler(call):
    id_rqst=call.message.text
    if call.data=='sec_exec':
        answer=markups.SECURITY_EXEC_MENU['sec_exec']
        bot.answer_callback_query(call.id, text='Good')         

        if google_sheets.sec_update_rqst(id_rqst=int(id_rqst), state=1):
            bot.send_message(call.message.chat.id, text=f'Статус заявки №{id_rqst}: Виконано')
            id_user=google_sheets.sec_get_id_user(int(id_rqst))
            
            #add comment
            comment=bot.send_message(call.message.chat.id, text='Введіть свій коментар')
            bot.register_next_step_handler(comment, sec_add_comment, int(id_rqst))

    elif call.data=='sec_cancel':
        answer=markups.SECURITY_EXEC_MENU['sec_cancel']
        bot.answer_callback_query(call.id, text='Ohhh')        

        if google_sheets.sec_update_rqst(id_rqst=int(id_rqst), state=2):            
            bot.send_message(call.message.chat.id, text=f'Статус заявки № {id_rqst}: Відхилено')
           
            # add comment of reason to cancel
            comment=bot.send_message(call.message.chat.id, text='Введіть свій коментар, причину відхилення')
            bot.register_next_step_handler(comment, sec_add_comment_cancel, int(id_rqst))
    
    # delete buttons 
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{id_rqst} {answer}.', reply_markup=None)
    #send result to id_user.chat from requests.sheet

def sec_add_comment(message, id_rqst):
    if google_sheets.sec_add_comment(id_rqst, message.text):
        bot.send_message(message.chat.id, text='Коментар доданий в таблицю')
        id_user=google_sheets.sec_get_id_user(int(id_rqst))
        bot.send_message(chat_id=id_user, text=f'Ваша заявка {id_rqst} виконана. Коментар: {message.text}')
    bot.send_message(message.chat.id, text='Оберіть дію', reply_markup=markups.markups.keyboard(markups.SECURITY_MENU))

def sec_add_comment_cancel(message, id_rqst):
    if google_sheets.sec_add_comment(id_rqst, message.text):
        bot.send_message(message.chat.id, text='Коментар доданий в таблицю')
        id_user=google_sheets.sec_get_id_user(int(id_rqst))
        bot.send_message(chat_id=id_user, text=f'Ваша заявка {id_rqst} відхилена. Коментар: {message.text}')
    bot.send_message(message.chat.id, text='Оберіть дію', reply_markup=markups.keyboard(markups.SECURITY_MENU))

##### /end security handlers

#### Users handlers
@bot.callback_query_handler(func=lambda call: call.data in markups.REGISTRATION.keys())
def handler_registration(call):
    if call.data=='rg_yes':
        bot.answer_callback_query(call.id, text='Good') 
        answer=markups.REGISTRATION['rg_yes']

        mes_for_tel_number='Відправте Ваш номер телефону для реєстрації у боті.'
        phone_number=bot.send_message(call.message.chat.id, text=mes_for_tel_number)
        
        bot.register_next_step_handler(phone_number, phone)
       
    elif call.data=='rg_no':
        bot.answer_callback_query(call.id, 'Ohhhh')
        answer=markups.REGISTRATION['rg_no']
        bot.send_message(call.message.chat.id, text='До побачення!')
    
    # delete buttons 
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=None)



##!!!REDO 
def phone(number):    
    correct_number=google_sheets.is_correct_number(number.text)
    #check is correct number
    if correct_number:
        if google_sheets.is_in_db_tenants(correct_number) :
            #check in db_users_telegram
            if google_sheets.is_number_in_user_telegram(correct_number)==False:
                google_sheets.add_user_id(number.chat.id, correct_number)
                bot.send_message(number.chat.id, text='Ви успішно зареєстровані')
                bot.send_message(number.chat.id, 'Оберіть дію: ', reply_markup=markups.keyboard(markups.REQUEST)) 
            else:
                bot.send_message(number.chat.id, text='За таким номером зареєстрований інший користувач. Зверніться до адміністрації')
        else:
            bot.send_message(number.chat.id, text='Ваш номер телефону не знайдено! Зверніться до адміністрації')
    
    else: #is incorrect, repeat it
        repeat_number=bot.send_message(number.chat.id, text='Введіть корректний номер телефону!')
        bot.register_next_step_handler(repeat_number, phone) 


@bot.callback_query_handler(func=lambda call: call.data in markups.REQUEST.keys())
def requests(call):
    if call.data=='rq_security':
        bot.answer_callback_query(call.id, 'Good') #!!!!!
        answer=markups.REQUEST['rq_security']

        bot.send_message(call.message.chat.id, text=google_sheets.security_contact())
        
    elif call.data=='rq_create':
        dict_rqst=dict()
        bot.answer_callback_query(call.id, 'Ok')
        answer=markups.REQUEST['rq_create']

        bot.send_message(call.message.chat.id, text='Оберіть мету заявки:', reply_markup=markups.keyboard(markups.TARGET))
        
    elif call.data=='rq_state':        
        #input number of requsest
        bot.answer_callback_query(call.id, 'Ok')
        answer=markups.REQUEST['rq_state']

        number=bot.send_message(call.message.chat.id, text='Введіть номер заявки')
        bot.register_next_step_handler(number, get_status_request)
        
    elif call.data=='rq_all_requests':
        bot.answer_callback_query(call.id, 'Ok')
        answer=markups.REQUEST['rq_all_requests']

        list_requests=google_sheets.get_list_rqsts_user(call.message.chat.id)
        if list_requests:
            for rqst in list_requests:
                bot.send_message(call.message.chat.id, text=rqst)
        else:
            bot.send_message(call.message.chat.id, text='Ваш список пустий')
    
    #delete buttons
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=None)
     

def get_status_request(number):
    if number.text.strip().isdigit():
        text=google_sheets.get_state_request(id_user=number.from_user.id, id_request=int(number.text))
        adress=google_sheets.get_rqst_adress(id_request=int(number.text)) \
            if google_sheets.is_rqst_of_user(number.from_user.id, int(number.text)) \
                else ''
    else:
        text='Введено некорректні дані!'
    bot.send_message(number.from_user.id, text=f'Статус заявки № {number.text} за адресою {adress}: "{text}"')
    return

############ target!!redo


@bot.callback_query_handler(func=lambda call: call.data in markups.TARGET.keys())
def handler_target(call):
    ## ['id_request', 'id_user', 'adress', 'telephone', 'target', 'number of avto', 'additional info', 'kpp', 'date', 'status']
    dict_rqst['id_request']=google_sheets.get_id_rqst()
    dict_rqst['id_user']=call.message.chat.id
    dict_rqst['adress']= google_sheets.get_adress(call.message.chat.id)
    dict_rqst['telephone']=google_sheets.get_telephone(call.message.chat.id)
    dict_rqst['date']=call.message.date
    dict_rqst['status']=0

    if call.data=='trg_taxi':
        answer=markups.TARGET['trg_taxi']
        dict_rqst['target']='Таксі'
        bot.answer_callback_query(call.id, 'Ok')
        num_auto=bot.send_message(call.message.chat.id, text='Введіть номер авто')                        
        bot.register_next_step_handler(num_auto, add_num_auto) # next input message
         

    elif call.data=='trg_curier':
        answer=markups.TARGET['trg_curier']        
        bot.send_message(call.message.chat.id, text='Виберіть опцію для кур`єра', reply_markup=markups.keyboard(markups.CURIER))
        
    
    elif call.data=='trg_guests': 
        answer=markups.TARGET['trg_guests']         
        bot.send_message(call.message.chat.id, text='Виберіть опцію для Гості', reply_markup=markups.keyboard(markups.GUESTS))
        

    elif call.data=='trg_parking_problem':
        answer=markups.TARGET['trg_parking_problem']         
        bot.send_message(call.message.chat.id, text='Виберіть опцію для Проблеми з парковкою', reply_markup=markups.keyboard(markups.PARKING))
        
    
    elif call.data=='trg_other':
        answer=markups.TARGET['trg_other']  
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['target']='Інше'
        dict_rqst['number of avto']=None                 
        
        info=bot.send_message(call.message.chat.id, text='Введіть інформацію:')
        bot.register_next_step_handler(info, add_kpp)
    
    #delete buttons  
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=None)


def add_num_auto(message): 
    dict_rqst['number of avto']=message.text
    bot.send_message(message.chat.id, text='Бажаєте ввести додаткову інформацію?', reply_markup=markups.keyboard(markups.INFO)) 
  

@bot.callback_query_handler(func=lambda call: call.data in markups.INFO.keys())
def handler_info(call):
    if call.data=='info_yes':
        answer=markups.INFO['info_yes']
        info=bot.send_message(call.message.chat.id, text='Введіть додаткову інформацію')
        bot.register_next_step_handler(info, add_kpp)
    elif call.data=='info_no':
        answer=markups.INFO['info_no']
        dict_rqst['additional info']=''
        bot.send_message(call.message.chat.id, text='Оберіть КПП:', reply_markup=markups.keyboard(markups.KPP))
    
    #delete buttons
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Бажаєте ввести додаткову інформацію? '+answer, reply_markup=None)


def add_kpp(id_user):
    dict_rqst['additional info']=id_user.text
    bot.send_message(id_user.chat.id, text='Оберіть КПП:', reply_markup=markups.keyboard(markups.KPP))    
    

@bot.callback_query_handler(func=lambda call: call.data in markups.KPP.keys())
def handler_kpp(call): 
    if call.data=='kpp_first':
        answer=markups.KPP['kpp_first']
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['kpp']=answer
    elif call.data=='kpp_second':
        answer=markups.KPP['kpp_second']
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['kpp']=answer
    elif call.data=='kpp_undef':
        answer=markups.KPP['kpp_undef']
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['kpp']=answer

    # delete buttons 
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=None)

    mes=bot.send_message(call.message.chat.id, text='Ваша заявка відправлена в обробку')
    create_rq(mes)
    list_surity=google_sheets.sec_get_list_id()

    ##redo!! push notifications
    if list_surity:
        for id_sec in list_surity:
            bot.send_message(id_sec, text='Отримано нову заявку')
    

@bot.callback_query_handler(func=lambda call: call.data in markups.CURIER.keys())
def handler_curier(call):       
    if call.data=='curier_no':
        answer= markups.CURIER['curier_no']
        bot.answer_callback_query(call.id, 'Good') 

        dict_rqst['target']=answer             
        dict_rqst['number of avto']=None
        info=bot.send_message(call.message.chat.id, text='Введіть інформацію про кур’єра:')
        bot.register_next_step_handler(info, add_kpp)

    elif call.data=='curier_yes':
        bot.answer_callback_query(call.id, 'Ok')
        answer= markups.CURIER['curier_yes']
        dict_rqst['target']=answer        
        num_auto=bot.send_message(call.message.chat.id, text='Введіть номер авто')                       
        bot.register_next_step_handler(num_auto, add_num_auto) # next input message

     # delete buttons 
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=None)


@bot.callback_query_handler(func=lambda call: call.data in markups.GUESTS.keys())
def handler_guests(call):      
    if call.data=='guests_no':
        answer=markups.GUESTS['guests_no']
        bot.answer_callback_query(call.id, 'Good') 
        dict_rqst['target']=answer 
        dict_rqst['number of avto']=None
        info=bot.send_message(call.message.chat.id, text='Введіть інформацію щодо гостей:')
        bot.register_next_step_handler(info, add_kpp)

    elif call.data=='guests_yes':
        answer=markups.GUESTS['guests_yes']
        bot.answer_callback_query(call.id, 'Ok')
        dict_rqst['target']=answer
        num_auto=bot.send_message(call.message.chat.id, text='Введіть номер авто')                       
        bot.register_next_step_handler(num_auto, add_num_auto) # next input message 

     # delete buttons 
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=None)


@bot.callback_query_handler(func=lambda call: call.data in markups.PARKING.keys())
def handler_parking(call): 
    target='Проблеми з парковкою.'     
    if call.data=='auto_blocked':
        answer=markups.PARKING['auto_blocked']
        target+=' Ваш авто заблокований' 

    elif call.data=='auto_incorrect_place':
        answer=markups.PARKING['auto_incorrect_place']
        target+=' Авто в недозволеному місці'

    bot.answer_callback_query(call.id, 'Ok')
    dict_rqst['target']=target
    num_auto=bot.send_message(call.message.chat.id, text='Введіть номер авто')                       
    bot.register_next_step_handler(num_auto, add_num_auto) # next input message 

     # delete buttons 
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=None)



# add request to table and send message to user
def create_rq(message): 
    request=[]
    for i in HEAD_RQST_SHEET:
        request.append(dict_rqst[i]) if i in dict_rqst.keys() else request.append(None)    
    google_sheets.add_request(request)    
    bot.send_message(message.chat.id, text=f'Ваша заявка № {request[0]} прийнята!')

##### end Users handlers/

bot.polling(non_stop=True)


