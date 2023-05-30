import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# authorize 
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client=gspread.authorize(credentials)


# connect to google sheets
SHEET_LINK='1-0S0jFCpWo2gk_ejeedk86O5TaSNrhSZaEmIpGnlIzo'
gs = gspread.service_account(filename='credentials.json')  # connect credentials
sh = gs.open_by_key(SHEET_LINK)  # connect sheetID
worksheet = sh.sheet1  # get 1st page

result=worksheet.get_all_records() # get all rows from page

print(result)



