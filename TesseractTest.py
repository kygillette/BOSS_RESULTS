from PIL import Image
from pytesseract import pytesseract
import hashlib
import shutil
import os
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json

#Access [FRND] Boss Timers sheet
scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\Super Kyle\Documents\Python Scripts\frnd-boss-results-8ec834ed771a.json", scopes) #access the json key you downloaded earlier
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("[FRND] Boss Timers")  #open sheet
sheet = sheet.sheet1  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

#screenshot paths
Boss_Results_SS_Path = r"C:\Users\Super Kyle\Pictures\Python Stuff"
Boss_Results_SS_Archive = r"C:\Users\Super Kyle\Pictures\Python Stuff\OLD_BOSS_RESULTS"

#Boss results log
Boss_Results_Log_Path = r"C:\Users\Super Kyle\Pictures\Python Stuff\OLD_BOSS_RESULTS\Boss_Results_log.txt"

# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# image_path = r"C:\Users\Super Kyle\Pictures\Python Stuff\2022-09-01_06-33-22.131.tiff"
# fetch screenshots
screenshots = os.listdir(Boss_Results_SS_Path)

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

#initializing variables
LAST_HASH = ''
unknown_boss = False
summoned_boss = False

for SS in screenshots:
    if SS == "OLD_BOSS_RESULTS":
        print("Skipping old folder")
    else:
        SS_PATH = Boss_Results_SS_Path + "\\" + SS
        SS_HASH = hash_file(SS_PATH)
        print(SS_HASH)

        if LAST_HASH == SS_HASH:
            print("Same SS - Skipped")

            #Write to Log
            with open(Boss_Results_Log_Path, 'a') as log_file:

                log_file.write(now_formatted + '\n')
                log_file.write(SS_HASH + '\n')
                log_file.write('Same HASH - SS Skiped\n')

        else:

            LAST_HASH = SS_HASH
            # Opening the image & storing it in an image object
            img = Image.open(SS_PATH)

            # Crop image to get top of boss results
            crop_rectangle = (240, 10, 600, 70 )
            cropped_img = img.crop(crop_rectangle)

            # Providing the tesseract executable
            # location to pytesseract library
            pytesseract.tesseract_cmd = path_to_tesseract

            # Passing the image object to image_to_string() function
            # This function will extract the text from the image
            text = pytesseract.image_to_string(cropped_img)

            #Print date & time stamp
            now = datetime.now()
            now_formatted = now.strftime("%m/%d/%Y %H:%M:%S")
            print(now_formatted)

            # Displaying the extracted text
            print(text[:-1])

            #Write to google sheet - sheet.update_acell('H4', now_formatted)
            if "Summoned" in text:
                summoned_boss = True
            else:

                if "Sanguineous" in text:
                    sheet.update_acell('H4', now_formatted)
                elif "Great Abyssal Hornbeast" in text:
                    sheet.update_acell('H5', now_formatted)
                elif "Terrorwood" in text:
                    sheet.update_acell('H6', now_formatted)
                elif "Heart of the Mountain" in text:
                    sheet.update_acell('H7', now_formatted)
                elif "Cistern Gorgon" in text:
                    sheet.update_acell('H8', now_formatted)
                elif "Lodestone" in text:
                    sheet.update_acell('H9', now_formatted)
                elif "Pit Dragon" in text:
                    sheet.update_acell('H10', now_formatted)
                elif "Speaker for the Dead" in text:
                    sheet.update_acell('H11', now_formatted)
                elif "Ancient Drowned Dragon" in text:
                    sheet.update_acell('H12', now_formatted)
                elif "Gargoyle Archon" in text:
                    sheet.update_acell('H13', now_formatted)
                elif "Aegis High Priestess" in text:
                    sheet.update_acell('H14', now_formatted)
                elif "Behemoth Basilisk" in text:
                    sheet.update_acell('H15', now_formatted)
                elif "Lore Bile" in text:
                    sheet.update_acell('H16', now_formatted)
                elif "Infernus" in text:
                    sheet.update_acell('H17', now_formatted)
                elif "Gatekeeper" in text:
                    sheet.update_acell('H18', now_formatted)
                elif "Terathan Goliath" in text:
                    sheet.update_acell('H19', now_formatted)
                elif "Emperor Dragon" in text:
                    sheet.update_acell('H20', now_formatted)
                elif "The Forgotten King" in text:
                    sheet.update_acell('H21', now_formatted)
                elif "Great Sunken Serpent" in text:
                    sheet.update_acell('H22', now_formatted)
                elif "Gargoyle Primogen" in text:
                    sheet.update_acell('H23', now_formatted)
                else:
                    unknown_boss = True

            #Write to Log
            with open(Boss_Results_Log_Path, 'a') as log_file:

                log_file.write(now_formatted + '\n')
                log_file.write(SS_HASH + '\n')
                log_file.write(text[:-1] + '\n')
                if unknown_boss:
                    log_file.write('Unknown boss was not witten to sheet\n')
                    unknown_boss = False

                if summoned_boss:
                    log_file.write('Summoned boss was not witten to sheet\n')
                    summoned_boss = False


            # Move SS after OCR
        shutil.move(SS_PATH, Boss_Results_SS_Archive)
