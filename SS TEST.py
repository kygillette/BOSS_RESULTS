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
from fuzzywuzzy import fuzz

# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = ImageGrab.grab(bbox=(20,80,658,400))
img = img.convert("L")
#img.show()
img.save("C:\BossResults\ss_1.png")

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

SS_PATH = r"C:\BossResults\ss_1.png"
SS_HASH = hash_file("C:\BossResults\ss_1.png")
print(SS_HASH)

# Crop image to get top of boss results
crop_rectangle = (220, 5, 600, 35 )
cropped_img_A = img.crop(crop_rectangle)
cropped_img_A.show()

# Crop image to get guild totalS
crop_rectangle = (460, 105, 520, 315 )
cropped_img_B = img.crop(crop_rectangle)
#cropped_img_B.show()

# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to image_to_string() function
# This function will extract the text from the image
textA = pytesseract.image_to_string(cropped_img_A)
# Passing the image object to image_to_string() function
# This function will extract the text from the image
textB = pytesseract.image_to_string(cropped_img_B)
# Displaying the extracted text
print(textA)
#print("Fuzzy ratio: " + str(fuzz.partial_ratio("Augis High Priestess", textA)))
print(textB)
