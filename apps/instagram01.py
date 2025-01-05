# -*- coding: utf-8 -*-
# pip install instagrapi 
# pip install Pillow


import os 
import sys 


os.environ['INSTAGRAM_CREDENTIAL_PATH'] = "H:\\My Drive\\__CREDENTIALS__\\INSTAGRAM\\credentials.json"
os.environ['INSTAGRAM_DOWNLOAD_PATH'] = 'C:\\Users\\innovata\\Downloads'


sys.path.append("D:\\pypjts\\iCrawler\\src")
from ipycrawl.crawlers import instagram 

# https://www.instagram.com/p/DEXQ4CpI2vA/?utm_source=ig_web_copy_link

cred = instagram.read_credientials()
print(cred)
# url = input("Input your Instagram URL: ")
# instagram.login()
# instagram.download(url)
