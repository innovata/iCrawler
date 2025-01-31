

import sys 
import os 
import pprint 
pp = pprint.PrettyPrinter(indent=2)


sys.path.append("D:\\pypjts\\iCrawler\\src")
from ipycrawl.crawlers.youtube._yt_dlp import *




# ============================================================
# 실행코드 
# ============================================================

# url = 'https://www.youtube.com/watch?v=gqSb1ne0ieM'
# url = "https://www.youtube.com/watch?v=Jrmb07ku6ZY&ab_channel=CristianyGabriella"
# url_pl = "https://youtube.com/playlist?list=PL_a1wRn79us-7t6zoK90sUrqM7RIG1qAR&feature=shared"
# url = input("Enter a YouTube video URL: ")
# download_video(url)
# extract_information(url)
# download_info(url, 'info.json')
# extract_audio(url)
# download_youtube_video_with_ffmpeg(url)
# download_audio_files_from_playlist(url_pl)

# generate_command(url)
# generate_command(url, type='audio')
# generate_command(url_pl)
# generate_command(url_pl, type='audio')
# generate_command(url_pl, type='audio', outpath="D:\\LatinDanceData\\Bachata_Demos\\Temp")

# download_audio(url, outpath=AUDIO_DOWNLOAD_PATH)
# download_video(url, outpath=VIDEO_DOWNLOAD_PATH)
# download_video(url, outpath="D:\\LatinDanceData\\Bachata_Demos\\CRISTIAN_GABRIELLA", mkdir=True)
# clean_outpath("CRISTIAN Y GABRIELLA | Bachata 🎵 MI HABITACIÓN - PRINCE ROYCE")





# url = 'https://www.youtube.com/watch?v=gqSb1ne0ieM'
# url = "https://www.youtube.com/watch?v=Jrmb07ku6ZY&ab_channel=CristianyGabriella"
# url = "https://youtube.com/playlist?list=PL_a1wRn79us-7t6zoK90sUrqM7RIG1qAR&feature=shared"
url = "https://www.youtube.com/playlist?list=PL_a1wRn79us-7t6zoK90sUrqM7RIG1qAR"




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


# generate_command_v2(url, options={}, only_audio=True)


# download_audio(url, outpath=AUDIO_DOWNLOAD_PATH)
# download_video(url, outpath=VIDEO_DOWNLOAD_PATH, mkdir=True)
# download_video(url, outpath="D:\\LatinDanceData\\Bachata_Demos\\CRISTIAN_GABRIELLA", mkdir=True)
# clean_outpath("CRISTIAN Y GABRIELLA | Bachata 🎵 MI HABITACIÓN - PRINCE ROYCE")
download_audio_files_from_playlist(url)