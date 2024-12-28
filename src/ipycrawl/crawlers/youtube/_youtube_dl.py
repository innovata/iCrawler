# -*- coding: utf-8 -*-

# GITHUB : https://github.com/ytdl-org/youtube-dl 



from pytube import YouTube

def download_youtube_video(url):
    try:
        yt = YouTube(url)

        # 다양한 스트림 시도
        for stream in yt.streams.filter(progressive=True, file_extension='mp4'):
            try:
                stream.download()
                print("다운로드 완료!")
                break
            except Exception as e:
                print(f"다운로드 실패: {e}")
    except Exception as e:
        print(f"다운로드 실패: {e}")

# 다운로드할 유튜브 영상 URL
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # 예시 URL

download_youtube_video(url)