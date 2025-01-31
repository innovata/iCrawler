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
# YouTube
################################################################

credentials_path = ''
video_dir = "D:\\GABRIELE_DRIVE\\Bachata_Demos\\Temp"
audio_dir = "D:\\GABRIELE_DRIVE\\LatinMusic\\Bachata"
audio_google_dir = "H:\\내 드라이브\\MEDIA_DRIVE\\MUSIC\\Latin_Music\\Bachata"

os.environ['YOUTUBE_CREDENTIAL_PATH'] = credentials_path
os.environ['YOUTUBE_VIDEO_DOWNLOAD_PATH'] = video_dir
os.environ['YOUTUBE_AUDIO_DOWNLOAD_PATH'] = audio_dir
os.environ['YOUTUBE_AUDIO_DOWNLOAD_GOOGLE_PATH'] = audio_google_dir




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



