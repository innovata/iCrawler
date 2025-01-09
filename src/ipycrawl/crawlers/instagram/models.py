# -*- coding: utf-8 -*-


# from ipycrawl.crawlers.instagram import _instagrapi
from . import _instagrapi






class InstaMedia():

    def __init__(self, url):
        self.url = url 

    def download(self):
        _instagrapi.download_video(self.url)






class InstaCollection():

    def __init__(self, url):
        self.url = url 


