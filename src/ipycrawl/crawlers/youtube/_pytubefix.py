# -*- coding: utf-8 -*-
# 구글 공식 API 를 사용하는 방법은 여기서 다루지 않는다.
# 써드파티 라이브러리를 이용하는 방법만 다룬다.



 


import os 
import pprint 
pp = pprint.PrettyPrinter(indent=2)


from ipycrawl.crawlers.youtube._pytubefix import YouTube 
from pytubefix.cli import on_progress
from moviepy.video.io import ffmpeg_tools






def download_video(url, _dir=os.getcwd()):
    yt = YouTube(url, on_progress_callback = on_progress)
    print('Title:', yt.title)
    print("Video ID:", yt.video_id)

    print(yt.check_availability())

    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    

    # 비디오파일 다운로드(오디오 없음) (360p 만 오디오까지 한번에 있기 때문에...)
    stream = select_highest_resolution(yt)
    if stream is None:
        print("ERROR | 원하는 고해상도 영상은 없다.")
    else:
        resolution = stream.__dict__['resolution']
        print('Resolution:', resolution)

        print('Downloading video...')
        video_path = stream.download(
            output_path=_dir, 
            filename='video.mp4',
        )

        # 오디오파일 다운로드
        stream = yt.streams.get_audio_only()
        bit_rate = stream.__dict__['abr']
        print('Bitrate:', bit_rate)

        print('Downloading audio...')
        audio_path = stream.download(
            output_path=_dir, 
            filename='audio', 
            mp3=True
        )
        
        # 비디오, 오디오 합치기
        print("Merging video + audio...")
        output_path = os.path.join(_dir, f"{yt.title}_({resolution},{bit_rate}).mp4")
        ffmpeg_tools.ffmpeg_merge_video_audio(
            video_path, audio_path, output_path, 
            vcodec='copy', acodec='copy', ffmpeg_output=False, logger='bar'
        )

        # 비디오/오디오 단독 파일들 삭제
        for filename in ['video.mp4', 'audio.mp3']:
            os.remove(os.path.join(_dir, filename))

        print(f"DONE | {output_path}")



def select_highest_resolution(yt):
    resolutions = ['1080p','720p']
    for res in resolutions:
        streams = yt.streams.filter(file_extension='mp4', resolution=res)
        if len(streams) > 0:
            return streams[0]



# 유투브 영상속 음원은 기본 128kbps 만 다운로드 된다.
# 다른 옵션은 존재하지 않는다.
def download_audio(url, _dir=os.getcwd()):
    yt = YouTube(url, on_progress_callback=on_progress)    
    print(yt.title)

    stream = yt.streams.get_audio_only()
    bit_rate = stream.__dict__['abr']
    # print(stream)
    # pp.pprint(stream.__dict__)
    print(f'Bit Rate: {bit_rate}')
    mp3file = stream.download(
        output_path=_dir, 
        filename=f"{yt.title}_{bit_rate}", 
        mp3=True
    )

    # 파일명에 추가정보 
    print(f'DONE | {mp3file}')
    return mp3file




