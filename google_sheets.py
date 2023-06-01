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
sh = client.open_by_key(ID_TABLE)  # connect sheetID

### Registration /
db_tenants = sh.sheet1  # def 1st sheet - tenant_database
ids_telegram=sh.worksheet('Лист2') # def 2nd sheet


LEN_OF_NUMBER=(9,13)

# check correct telephone number
def is_correct_number(message:str)->int:
    
    message=''.join(message.strip().split())

    #check and return last 10 digits of number
    if len(message) in range(*LEN_OF_NUMBER) and message[-10:].isdigit():
        return int(message.strip()[-10:])
    else:
        return -1
    

# check number of telephon in tenant_database
def is_in_db_tenants( tel_number:int )->bool:
    
    for row in db_tenants.get_all_records():       
       if row['telephon']%10**10==tel_number:
           return True
    return False

# is tel in db_tenants to add id_user_telegram and tel
def add_user_id(user_id, telephone)->bool:

    if user_id not in ids_telegram.col_values(col=1):
        ids_telegram.append_row(user_id, telephone)
        return True
    else: 
        return False

### /end Registration

#


#Tests 
'''
values=('253648', '56485235458')
print(add_user_id(*values))
print(ids_telegram.get_all_records())


tel='380664442233'
print(is_correct_number(tel))
#print( is_in_db_tenants(tel))

'''

