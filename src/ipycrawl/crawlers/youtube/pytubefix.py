# -*- coding: utf-8 -*-
# 구글 공식 API 를 사용하는 방법은 여기서 다루지 않는다.
# 써드파티 라이브러리를 이용하는 방법만 다룬다.






import os 
import pprint 
pp = pprint.PrettyPrinter(indent=2)


from pytubefix import YouTube 
from pytubefix.cli import on_progress






def download_video(url, _dir=os.getcwd()):
    yt = YouTube(url, on_progress_callback = on_progress)
    print('Title:', yt.title)
    
    stream = select_highest_resolution(yt)
    resolution = stream.__dict__['resolution']
    print('Resolution:', resolution)
    # mp4file = os.path.join(_dir, f"{yt.title}_{resolution}.mp4")
    # print(f"Download File: {mp4file}")


    mp4file = stream.download(output_path=_dir, filename=f"{yt.title}_{resolution}.mp4", mp3=True)
    print(f"DONE | {mp4file}")

    # 파일명수정
    # try:
    #     os.rename(srcfile, dstfile)
    #     print(f'DONE | {dstfile}')
    # except OSError as e:
    #     print(f"ERROR | {e}")



def select_highest_resolution(yt):
    for st in yt.streams:
        # print('-'*100)
        # print(type(st))
        # print(st)
        if st.__dict__['resolution'] == '1080p':
            # pp.pprint(st.__dict__)
            break 
    return st



# 유투브 영상속 음원은 기본 128kbps 만 다운로드 된다.
# 다른 옵션은 존재하지 않는다.
def download_mp3(url, _dir=os.getcwd()):
    yt = YouTube(url, on_progress_callback=on_progress)    
    print(yt.title)

    stream = yt.streams.get_audio_only()
    bit_rate = stream.__dict__['abr']
    # print(stream)
    # pp.pprint(stream.__dict__)
    print(f'Bit Rate: {bit_rate}')
    stream.download(mp3=True)

    # 파일명에 추가정보 
    print(f'DONE | {os.path.join(_dir, f"{yt.title}_({bit_rate}).mp3")}')




