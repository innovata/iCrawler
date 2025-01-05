# -*- coding: utf-8 -*-
# Python Package instagrapi 를 이용한 크롤러. 



import os 
import json 
import pprint 
pp = pprint.PrettyPrinter(indent=2)


from instagrapi import Client
# from PyQt5.QtCore import *


# from ipylib.idebug import *


CREDENTIAL_PATH = os.environ['INSTAGRAM_CREDENTIAL_PATH']
DOWNLOAD_PATH = os.environ['INSTAGRAM_DOWNLOAD_PATH']



CLIENT = Client()



def read_credientials():
    with open(CREDENTIAL_PATH, 'r', encoding='utf-8') as f:
        d = json.loads(f.read())
        f.close()
    return d 


def login():
    cred = read_credientials()
    v = CLIENT.login(cred['ID'], cred['PASSWORD'])
    print({'로그인결과': v})


def get_videoUrl(media):
    if getattr(media, 'video_url'): url = media.video_url
    elif len(media.resources) > 0: url = media.resources[0].video_url
    else: raise
    print({'video_url': url})
    return url


def download(url):
    pk = CLIENT.media_pk_from_url(url)
    media = CLIENT.media_info(pk)
    pp.pprint(media.__dict__)

    video_url = get_videoUrl(media)

    CLIENT.video_download_by_url(video_url, folder=DOWNLOAD_PATH)


# def collections():



class Media:

    def __init__(self, media):
        super().__init__()
        self.media = media
    def download(self, path=None):
        path = DOWNLOAD_PATH if path is None else path
        video_url = get_videoUrl(self.media)
        CLIENT.video_download_by_url(video_url, folder=path)
