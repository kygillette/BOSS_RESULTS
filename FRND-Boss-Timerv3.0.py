from PIL import ImageGrab
from PIL import Image, ImageEnhance, ImageOps
from pytesseract import pytesseract
import hashlib
import shutil
import os
from datetime import datetime
from datetime import timedelta
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import time
from tkinter import *
import sys
from fuzzywuzzy import fuzz

#Access [FRND] Boss Timers sheet
scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(r"C:\SheetsAPIKEY\frnd-boss-results-8ec834ed771a.json", scopes) #access the json key you downloaded earlier
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("[FRND] Boss Timers")  #open sheet
sheet = sheet.sheet1  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

#screenshot paths
Boss_Results_SS_Path = r"C:\BossResults"

#Boss results log
Boss_Results_Log_Path = r"C:\BossResults\Boss_Results_log.txt"

# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Create an instance of tkinter frame
win= Tk()

# Set the size of the Tkinter window
win.geometry("300x200")

# variable which runs boss results program in infinite loop
run= True

#initializing variables
LAST_HASH = ''
unknown_boss = False
summoned_boss = False

#Functions to run boss results flow
def boss_results():

   global LAST_HASH
   global unknown_boss
   global summoned_boss
   global now_formatted

   if run:

       img = ImageGrab.grab(bbox=(20,80,658,400))
       #img.show()
       img = img.convert("L")
       img.save("C:\BossResults\ss_1.png")
       CURRENT_HASH = hash_file("C:\BossResults\ss_1.png")
       #print("Current Hash: " + CURRENT_HASH)

       if CURRENT_HASH != LAST_HASH:
           #print("NEW HASH")
           LAST_HASH = CURRENT_HASH

           # Crop image to get top of boss results
           crop_rectangle = (220, 5, 600, 35 )
           cropped_img_A = img.crop(crop_rectangle)
           #cropped_img_A.show()

           # Crop image to get guild totals
           crop_rectangle = (460, 105, 520, 315 )
           cropped_img_B = img.crop(crop_rectangle)
           #cropped_img_B.show()

           # Providing the tesseract executable
           # location to pytesseract library
           pytesseract.tesseract_cmd = path_to_tesseract

           # Passing the image object to image_to_string() function
           # This function will extract the text from the image
           textA = pytesseract.image_to_string(cropped_img_A)
           textB = pytesseract.image_to_string(cropped_img_B)
           # Displaying the extracted text
           print(textA)
           print(textB)

           #Print date & time stamp
           if "FRND" in textB:
               now = datetime.now()
               now = now - timedelta(minutes=5)
               now_formatted = now.strftime("%m/%d/%Y %H:%M:%S")
               print(now_formatted)

           else:
               now = datetime.now()
               now = now - timedelta(hours=1)
               now_formatted = now.strftime("%m/%d/%Y %H:%M:%S")
               print(now_formatted)

           if "Summoned" in textA:
               summoned_boss = True

           else:

               if "Sanguineous" in textA or "Sangvineous" in textA:
                   sheet.update_acell('H4', now_formatted)
               elif "Great Abyssal Hornbeast" in textA or "Abyssal" in textA or "Hornbeast" in textA:
                   sheet.update_acell('H5', now_formatted)
               elif "Terrorwood" in textA:
                   sheet.update_acell('H6', now_formatted)
               elif "Heart of the Mountain" in textA or "Heart" in textA or "of" in textA or "Mountain" in textA:
                   sheet.update_acell('H7', now_formatted)
               elif "Cistern Gorgon" in textA or "Cistern" in textA or "Gorgon" in textA:
                   sheet.update_acell('H8', now_formatted)
               elif "Lodestone" in textA:
                   sheet.update_acell('H9', now_formatted)
               elif "Pit Dragon" in textA or "Pit" in textA:
                   sheet.update_acell('H10', now_formatted)
               elif "Speaker for the Dead" in textA or "Speaker" in textA or "for" in textA or "Dead" in textA:
                   sheet.update_acell('H11', now_formatted)
               elif "Ancient Drowned Dragon" in textA or "Aneient" in textA or "Ancient" in textA or "Drowned" in textA or "Dragon" in textA:
                   sheet.update_acell('H12', now_formatted)
               elif "Gargoyle Archon" in textA or "Archon" in textA:
                   sheet.update_acell('H13', now_formatted)
               elif "Aegis High Priestess" in textA or "Aegis" in textA or "High" in textA or "Priestess" in textA or "Regis" in textA:
                   sheet.update_acell('H14', now_formatted)
               elif "Behemoth Basilisk" in textA or "Behemoth" in textA or "Basilisk" in textA:
                   sheet.update_acell('H15', now_formatted)
               elif "Lord Bile" in textA or "Lord" in textA or "Bile" in textA:
                   sheet.update_acell('H16', now_formatted)
               elif "Infernus" in textA:
                   sheet.update_acell('H17', now_formatted)
               elif "Gatekeeper" in textA:
                   sheet.update_acell('H18', now_formatted)
               elif "Terathan Goliath" in textA or "Goliath" in textA or "Terathan" in textA:
                   sheet.update_acell('H19', now_formatted)
               elif "Emperor Dragon" in textA or "Emperor" in textA:
                   sheet.update_acell('H20', now_formatted)
               elif "The Forgotten King" in textA or "Forgotten" in textA or "King" in textA:
                   sheet.update_acell('H21', now_formatted)
               elif "Great Sunken Serpent" in textA or "Sunken" in textA or "Serpent" in textA:
                   sheet.update_acell('H22', now_formatted)
               elif "Gargoyle Primogen" in textA or "Primogen" in textA:
                   sheet.update_acell('H23', now_formatted)
               else:
                   unknown_boss = True

           #Write to Log
           with open(Boss_Results_Log_Path, 'a') as log_file:


               if unknown_boss:
                   log_file.write('UnknownBoss: ' + 'Unknown boss was not witten to sheet\n')
                   log_file.write('BossFound: ' + now_formatted + '\n')
                   log_file.write('BossFound: ' + CURRENT_HASH + '\n')
                   log_file.write('BossFound: ' + textA[:-1] + '\n')
                   unknown_boss = False
               elif summoned_boss:
                   log_file.write('SummonedBoss: ' + 'Summoned boss was not witten to sheet\n')
                   log_file.write('BossFound: ' + now_formatted + '\n')
                   log_file.write('BossFound: ' + CURRENT_HASH + '\n')
                   log_file.write('BossFound: ' + textA[:-1] + '\n')
                   summoned_boss = False
               else:
                   log_file.write('BossFound: ' + 'Boss was witten to sheet\n')
                   log_file.write('BossFound: ' + now_formatted + '\n')
                   log_file.write('BossFound: ' + CURRENT_HASH + '\n')
                   log_file.write('BossFound: ' + textA[:-1] + '\n')

       #else:
            #print("SAME BOSS RESULTS - SKIPPED")

            #Write to Log
            #with open(Boss_Results_Log_Path, 'a') as log_file:

                #log_file.write(now_formatted + '\n')
                #log_file.write(CURRENT_HASH + '\n')
                #log_file.write('SAME BOSS RESULTS - SKIPPED\n')
   else:
       sys.exit("Boss Results Script Ended")

   # After 15 sec call the boss_results() again
   win.after(5000, boss_results)
def start():
   global run
   run= True

def stop():
   global run
   run= False
   Label(win, text="Shutting Down", font= ('Helvetica 10 bold')).pack()

#Function returns SHA-1 hash of the file passed to it
def hash_file(filename):

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:

        #loop till the end of the File
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()

# Create buttons to trigger the starting and ending of the loop
start= Button(win, text= "Start", command= start)
start.pack(padx= 10)
stop= Button(win, text= "Stop", command= stop)
stop.pack(padx= 15)
Label(win, text="Running", font= ('Helvetica 10 bold')).pack()

if run:
    win.after(10000, boss_results)
    win.mainloop()

else:
    sys.exit("Boss Results Script Ended")
