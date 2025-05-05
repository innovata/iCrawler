# -*- coding: utf-8 -*-
# pip install moviepy

import os 
from urllib.parse import urlparse
from pathlib import WindowsPath
import json 
import pprint
pp = pprint.PrettyPrinter(indent=2)



from moviepy.video.io import ffmpeg_tools




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