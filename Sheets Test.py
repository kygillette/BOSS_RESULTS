from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
from datetime import datetime

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\Super Kyle\Documents\Python Scripts\frnd-boss-results-8ec834ed771a.json", scopes) #access the json key you downloaded earlier
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("[FRND] Boss Timers")  #open sheet
sheet = sheet.sheet1  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

#all_cells = sheet.range('A3:H23')

#for cell in all_cells:
#    print(cell.value)
now = datetime.now()
now_formatted = now.strftime("%m/%d/%Y %H:%M:%S")
sheet.update_acell('H4', now_formatted)
