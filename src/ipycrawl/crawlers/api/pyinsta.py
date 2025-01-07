# -*- coding: utf-8 -*-
from instagrapi import Client
from PyQt5.QtCore import *


from ipylib.idebug import *



CLIENT = Client()
DOWNLOAD_PATH = 'C:\\Users\\innovata\\Downloads'



def login():
    v = CLIENT.login('ahoragabriele@gmail.com', '!5272doubleO')
    print({'로그인결과':v})


def get_videoUrl(media):
    if getattr(media, 'video_url'): url = media.video_url
    elif len(media.resources) > 0: url = media.resources[0].video_url
    else: raise
    print({'video_url': url})
    return url


def download(url, path):
    pk = CLIENT.media_pk_from_url(url)
    media = CLIENT.media_info(pk)
    dbg.dict(media)

    video_url = get_videoUrl(media)

    CLIENT.video_download_by_url(video_url, folder=path)


# def collections():



class Media:

    def __init__(self, media):
        super().__init__()
        self.media = media
    def download(self, path=None):
        path = DOWNLOAD_PATH if path is None else path
        video_url = get_videoUrl(self.media)
        CLIENT.video_download_by_url(video_url, folder=path)
