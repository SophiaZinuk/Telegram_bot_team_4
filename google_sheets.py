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
def is_user_telegram(user_id)->bool:
    db_sheets=autorize()
    users_telegram=db_sheets[1]
    return True if str(user_id) not in users_telegram.col_values(col=1) else False


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
    tel= security.cell(2,4).value
    return f'Звернутися до охорони можна за телефоном: {tel}'

def add_request(*args):
    pass

def get_state_request(id_user, id_request):
    states=('В обробці', 'Оброблено', 'Відхилено')
    pass

#### /end Request


#Tests 

print(security_contact())
#values=('236248', '56253525524458')
#print(add_user_id(*values))



#tel='380664442243'
#t=is_correct_number(tel)
#print(t)
#if t!=-1:
  #  print(is_in_db_tenants(t))



