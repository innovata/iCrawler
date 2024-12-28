# -*- coding: utf-8 -*-

# GITHUB : 
# DOC : https://pytube.io/en/latest/ 


from pytube import YouTube

def download_youtube_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download()
        print("다운로드 완료!")
    except Exception as e:
        print(f"다운로드 실패: {e}")

# 다운로드할 유튜브 영상 URL
# url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # 예시 URL
url = input("Enter a YouTube video URL: ")

download_youtube_video(url)