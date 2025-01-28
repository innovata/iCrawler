# -*- coding: utf-8 -*-
import os 
import platform 



COMPUTER_NAME = platform.uname().node
print('COMPUTER_NAME: ', COMPUTER_NAME)



################################################################
# FFMPEG  
################################################################

if COMPUTER_NAME == "RYZEN9-X570-AORUS-ELITE":
    ffmpeg_path = "C:\\FFmpeg\\ffmpeg-7.1-full_build\\bin"
elif COMPUTER_NAME == "LX3-JLE69-KOR":
    ffmpeg_path = "C:\\FFmpeg\\ffmpeg-2024-12-27-git-5f38c82536-full_build\\bin"

os.environ['FFMPEG_BIN_LOCATION'] = ffmpeg_path




################################################################
# Youtube
################################################################

credentials_path = ''
VIDEO_DOWNLOAD_PATH = "D:\\GABRIELE_DRIVE\\Bachata_Demos\\Temp"
AUDIO_DOWNLOAD_PATH = "D:\\GABRIELE_DRIVE\\LatinMusic\\Bachata"
AUDIO_GOOGLE_DRIVE_PATH = "H:\\내 드라이브\\MEDIA_DRIVE\\Latin_Music\\Bachata"

os.environ['YOUTUBE_CREDENTIAL_PATH'] = credentials_path
os.environ['YOUTUBE_VIDEO_DOWNLOAD_PATH'] = VIDEO_DOWNLOAD_PATH
os.environ['YOUTUBE_AUDIO_DOWNLOAD_PATH'] = AUDIO_DOWNLOAD_PATH
os.environ['YOUTUBE_AUDIO_DOWNLOAD_GOOGLE_PATH'] = AUDIO_GOOGLE_DRIVE_PATH




################################################################
# Instagram 
################################################################

if COMPUTER_NAME == "RYZEN9-X570-AORUS-ELITE":
    credentials_path = "J:\\내 드라이브\\__CREDENTIALS__\\INSTAGRAM\\credentials.json"
    download_path = "D:\\__GABRIELE_DRIVE__\\LatinDanceData\\Instagram"
elif COMPUTER_NAME == "LX3-JLE69-KOR":
    credentials_path = "H:\\My Drive\\__CREDENTIALS__\\INSTAGRAM\\credentials.json"
    download_path = "D:\\GABRIELE_DRIVE\\Instagram" 

os.environ['INSTAGRAM_CREDENTIAL_PATH'] = credentials_path
os.environ['INSTAGRAM_DOWNLOAD_PATH'] = download_path



