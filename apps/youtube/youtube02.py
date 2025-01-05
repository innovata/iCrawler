

import sys 
import os 
import pprint 
pp = pprint.PrettyPrinter(indent=2)
sys.path.append("D:\\pypjts\\iCrawler\\src")


# LX3-JLE69-KOR
os.environ["FFMPEG_LOCATION"] = "C:\\FFmpeg\\ffmpeg-2024-12-27-git-5f38c82536-full_build\\bin"
# pp.pprint(os.environ.__dict__)
VIDEO_DOWNLOAD_PATH = "D:\\LatinDanceData\\Bachata_Demos\\Temp"
AUDIO_DOWNLOAD_PATH = "D:\\LatinDanceData\\LatinMusic\\Bachata"
AUDIO_GOOGLE_DRIVE_PATH = "H:\\내 드라이브\\MEDIA_DRIVE\\Latin_Music\\Bachata"



from ipycrawl.crawlers.youtube._yt_dlp import *




# url = 'https://www.youtube.com/watch?v=gqSb1ne0ieM'
# url = "https://www.youtube.com/watch?v=Jrmb07ku6ZY&ab_channel=CristianyGabriella"
# url = "https://youtube.com/playlist?list=PL_a1wRn79us-7t6zoK90sUrqM7RIG1qAR&feature=shared"
url = input("Enter a YouTube video URL: ")


# download_video(url)
# extract_information(url)
# download_info(url, 'info.json')
# extract_audio(url)
# download_youtube_video_with_ffmpeg(url)
# download_audio_files_from_playlist(url)

# generate_command(url)
# generate_command(url, type='audio')
# generate_command(url)
# generate_command(url, type='audio')
# generate_command(url, type='audio', outpath="D:\\LatinDanceData\\Bachata_Demos\\Temp")

# download_audio(url, outpath=AUDIO_DOWNLOAD_PATH)
download_video(url, outpath=VIDEO_DOWNLOAD_PATH, mkdir=True)
# download_video(url, outpath="D:\\LatinDanceData\\Bachata_Demos\\CRISTIAN_GABRIELLA", mkdir=True)
# clean_outpath("CRISTIAN Y GABRIELLA | Bachata 🎵 MI HABITACIÓN - PRINCE ROYCE")