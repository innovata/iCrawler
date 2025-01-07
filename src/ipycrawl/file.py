# -*- coding: utf-8 -*-
# pip install moviepy

import os 
from urllib.parse import urlparse
from pathlib import WindowsPath
import json 
import pprint
pp = pprint.PrettyPrinter(indent=2)


import requests

from moviepy.video.io import ffmpeg_tools






def download(url, _dir, method='GET'):
    o = urlparse(url)
    print(o)
    filename = os.path.basename(o.path)

    res = requests.request(method, url)
    print(res)
    # pp.pprint(res.__dict__)
    # print(res.content.strip())
    
    if res.status_code == 200:
        # _dir = os.path.join('c:\pypjts', 'iCrawler', 'Data')
        os.makedirs(_dir, exist_ok=True)
        filepath = os.path.join(_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(res.content.strip())

        print('Downloaded. ' + filepath)
    else: 
        pp.pprint(res.__dict__)
        raise 



def read_json(filepath):
    with open(str(WindowsPath(filepath)), mode='r', encoding='utf-8') as f:
        js = json.loads(f.read())
        f.close()
    return js 



# 비디오, 오디오 합치기
def merge_video_audio(video_file, audio_file, dstfile):
    print("Merging video + audio...")
    ffmpeg_tools.ffmpeg_merge_video_audio(
        video_file, audio_file, dstfile, 
        vcodec='copy', acodec='copy', ffmpeg_output=False, logger='bar'
    )