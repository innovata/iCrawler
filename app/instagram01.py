# -*- coding: utf-8 -*-



import os 
import sys 
import platform 


COMPUTER_NAME = platform.uname().node
print('COMPUTER_NAME: ', COMPUTER_NAME)

if COMPUTER_NAME == "RYZEN9-X570-AORUS-ELITE":
    os.environ['INSTAGRAM_CREDENTIAL_PATH'] = "J:\\내 드라이브\\__CREDENTIALS__\\INSTAGRAM\\credentials.json"
    os.environ['INSTAGRAM_DOWNLOAD_PATH'] = "D:\\LatinDanceData\\Instagram"
    
elif COMPUTER_NAME == "":
    os.environ['INSTAGRAM_CREDENTIAL_PATH'] = "H:\\My Drive\\__CREDENTIALS__\\INSTAGRAM\\credentials.json"
    os.environ['INSTAGRAM_DOWNLOAD_PATH']


sys.path.append("D:\\pypjts\\iCrawler\\src")
from ipycrawl.crawlers.instagram import _instagrapi 



# 영상 다운로드
# url = "https://www.instagram.com/p/DEdEkCAonkF/?utm_source=ig_web_copy_link"
# url = "https://www.instagram.com/reel/DEaGMQkCH3S/?utm_source=ig_web_copy_link"

# 이미지 다운로드
url = "https://www.instagram.com/p/DEXQ4CpI2vA/?utm_source=ig_web_copy_link"

# 사용자 입력
# url = input("Input your Instagram URL: ")

_instagrapi.login('ghost')
# _instagrapi.download_video(url)
_instagrapi.download_image(url)
