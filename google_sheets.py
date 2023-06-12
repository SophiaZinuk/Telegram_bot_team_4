#import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# authorize 
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client=gspread.authorize(credentials)


# connect to google sheets
ID_TABLE='1-0S0jFCpWo2gk_ejeedk86O5TaSNrhSZaEmIpGnlIzo'
LEN_OF_NUMBER=(9,13)

# connect to table and return sheets list
def autorize()->tuple:
    db=client.open_by_key(ID_TABLE)  # connect sheetID
    return tuple(db.worksheets())


### Registration /

# check correct telephone number
def is_correct_number(message:str)->str:
    
    message=''.join(message.strip().split())

    #check and return last 10 digits of number
    if len(message) in range(*LEN_OF_NUMBER) and message[-10:].isdigit():
        return message.strip()[-10:]
    else:
        return False
    

# check number of telephon in tenant_database
def is_in_db_tenants( tel_number:str )->bool:
    db_sheets=autorize()
    tel_nums=db_sheets[0].col_values(col=3)
    for i in range(1, len(tel_nums)):       
        if tel_number in tel_nums[i]:
            return True 
    return False

# is tel in db_tenants to add id_user_telegram and tel
def is_number_in_user_telegram(num_tel)->bool:
    db_sheets=autorize()
    users_telegram=db_sheets[1]
    return True if str(num_tel) in users_telegram.col_values(col=2) else False
        

def is_user(user_id)->bool:
    db_sheets=autorize()
    users_telegram=db_sheets[1]
    return True if str(user_id) in users_telegram.col_values(col=1) else False

# add user_telegram_id and telephone into table
def add_user_id(user_id, telephone)->bool:
    db_sheets=autorize()
    users_telegram=db_sheets[1]
    users_telegram.append_row(values=(user_id, telephone))
        
### /end Registration


#### Request/
def security_contact()->str:
    db_sheets=autorize()
    security=db_sheets[2]
    tel=str(security.cell(2,4).value)
    return f'Звернутися до охорони можна за телефоном: {tel}'

def get_telephone(id_user_telegr):
    db_sheets=autorize()
    telegram=db_sheets[1]
    telephone=[str(row['telephon']) for row in telegram.get_all_records() if str(id_user_telegr) in str(row['id_user_telegram'])]
    return telephone[0]

def get_adress(id_user_telegr):
    db_sheets=autorize()
    info_tenants=db_sheets[0]    
    tel=get_telephone(id_user_telegr)
    adress=[row['adress'] for row in info_tenants.get_all_records() if tel in str(row['telephon'])]
    return adress[0]

def get_id_rqst():
    db_sheets=autorize()
    rqst=db_sheets[4]
    last_id=rqst.get_values()[-1][0]
    id=int(last_id)+1 if last_id.strip().isdigit() else 1
    return id

def add_request(request: tuple):
    db_sheets=autorize()
    rqst=db_sheets[4]
    rqst.append_row(values=request)

def is_rqst_of_user(id_user, id_request):
    db_sheets=autorize()
    rqst=db_sheets[4]
    for row in rqst.get_all_records():
        if row['id_user']==id_user and row['id_request']==id_request :
            return True
    return False
    

def get_state_request(id_user, id_request): ###!!!redone
    states=('В обробці', 'Оброблено', 'Відхилено')
    db_sheets=autorize()
    rqst=db_sheets[4]
    if is_rqst_of_user(id_user, id_request):
        for row in rqst.get_all_records():
            if row['id_user']==id_user and row['id_request']==id_request :
                return states[row['status']]
    else:      
        return 'Заявку не знайдено!'

def get_rqst_adress(id_request):
    db_sheets=autorize()
    rqst=db_sheets[4]
    for row in rqst.get_all_records():
        if row['id_request']==id_request :
            return row['adress']    
    return 'Адресу не знайдено!'


def get_head():
    db_sheets=autorize()
    rqst=db_sheets[4]
    return rqst.row_values(1)

#ADD history of requests for user
def get_list_rqsts_user(id_user: int):
    states=('В обробці', 'Оброблено', 'Відхилено')
    db_sheets=autorize()
    sec_rqsts=db_sheets[4]
    list_rqsts=['№'+str(row['id_request'])+' '+row['adress']+' '+row['target']+' '+states[row['status']]+' '+row['comments']\
                for row in sec_rqsts.get_all_records() if row['id_user']==id_user ]
    return list_rqsts
    

#### /end Request

#### /Security

def check_security(id_user):
    db_sheets=autorize()
    security=db_sheets[2]
    return True if str(id_user) in security.col_values(col=2) else False

def sec_get_list_requests():
    db_sheets=autorize()
    sec_rqsts=db_sheets[4]
    list_rqsts=['№'+str(row['id_request'])+' '+row['adress']+' '+row['target']+' '+str(row['number of avto'])\
                for row in sec_rqsts.get_all_records() if row['status']==0 ]
    return list_rqsts

def sec_get_list_id_requests():
    db_sheets=autorize()
    sec_rqsts=db_sheets[4]
    list_id_rqsts=[row['id_request'] for row in sec_rqsts.get_all_records() if row['status']==0 ]
    return list_id_rqsts

# change status of request
def sec_update_rqst(id_rqst:int, state:int):
    db_sheets=autorize()
    sec_rqsts=db_sheets[4]
    for i in range(len(sec_rqsts.col_values(1))):
        if str(id_rqst)==sec_rqsts.col_values(col=1)[i]:
            sec_rqsts.update_cell(i+1, 10, state)
            return True
    return False
    
def sec_get_id_user(id_rqst:int):
    db_sheets=autorize()
    sec_rqsts=db_sheets[4]
    for row in sec_rqsts.get_all_records():
        if row['id_request']==id_rqst:
            return row['id_user']
    return None

# add security comment to request
def sec_add_comment(id_rqst:int, message:str):
    db_sheets=autorize()
    sec_rqsts=db_sheets[4]
    for i in range(len(sec_rqsts.col_values(1))):
        if str(id_rqst)==sec_rqsts.col_values(col=1)[i]:
            sec_rqsts.update_cell(i+1, 11, message)
            return True
    return False

#####/end Security


#Tests 
#print(sec_add_comment(22, 'khjghfhg'))
#print(sec_get_id_user(25))
#sec_update_rqst(16, 1)
#print(type(sec_get_list_id_requests()[0]))
#print(check_security('253556'))
#print(get_rqst_adress(11))
#print(get_head())
#print(get_state_request(id_user=6259460200, id_request=1))
#print(get_id_rqst())
#get_adress('6259460200')
#print(security_contact())
#values=('236248', '56253525524458')
#print(add_user_id(*values))



#tel='380664442243'
#t=is_correct_number(tel)
#print(t)
#if t!=-1:
  #  print(is_in_db_tenants(t))



