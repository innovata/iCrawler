# -*- coding: utf-8 -*-
from urllib.parse import urlparse, parse_qs
import json
import re
import os
from pathlib import PureWindowsPath, PurePosixPath
from time import sleep


import requests
from bs4 import BeautifulSoup
import pandas as pd
from PyQt5.QtCore import *


from idebug import *
from ipylib.ipath import *
from dataengineer.database import *
from dataengineer.models import *
from dataengineer import models


from youtube.base import *
from youtube.Lib import *
from youtube.models import *
from y2mate import *
from youtube.fhandler import *


__all__ = [
    'Playlist',
    'Video',
    'MusicPlayer',
]


class Playlist(BaseQWorker):
    fetched = pyqtSignal()
    downloaded = pyqtSignal()

    @ctracer
    def __init__(self, name):
        super().__init__()
        self._identify(name)
        # self.fetched.connect(self._setup_videos)

    @ctracer
    def _identify(self, name):
        cursor = Playlists().find({'name':name}, limit=1)
        data = list(cursor)
        pp.pprint(data)
        for k,v in data[0].items(): setattr(self, k, v)

    @classmethod
    def rename(self, name): DataModel('Playlists').update_one({'pid':self.pid}, {'$set':{'name':name}})
    @classmethod
    def delete(self):
        DataModel('Playlists').delete_one({'pid':self.pid})
        DataModel('PlaylistVideoMap').delete_many({'pid':self.pid})

    @property
    def Videos(self): return DataModel('Videos')

    @ctracer
    def fetch(self):
        # 구글계정없이 액세스할 수 있는 'WatchURL'을 사용해야한다
        try:
            r = requests.get(self.url)
            # dbg.dict(r)
            self.meta = PlaylistMeta(r.text)

            # Playlist-Video 매핑 정보 저장
            model = DataModel('PlaylistVideoMap')
            for d in self.meta.data:
                vid, idx = d['vid'], d['index']
                f = {'pid':self.pid, 'vid':vid}
                doc = f.copy()
                doc.update({'idx':idx})
                model.update_one(f, {'$set':doc}, True)

            # Video 정보 저장
            model = DataModel('Videos')
            for d in self.meta.data:
                del d['index']
                f = {'vid':d['vid']}
                model.update_one(f, {'$set':d}, True)
        except Exception as e:
            logger.error([self, e])
            raise
        else:
            self.fetched.emit()
    @ctracer
    def _setup_videos(self):
        model = DataModel('PlaylistVideoMap')
        cursor = model.find({'pid':self.pid})
        self.VideoObjects = {}
        for d in list(cursor):
            vid, idx = d['vid'], d['idx']
            v = Video({'vid':vid})
            v.idx = idx
            self.VideoObjects.update({v.vid: v})

    @property
    def PlaylistURL(self): return f'https://www.youtube.com/playlist?list={self.pid}'
    @property
    def WatchURL(self): return self.url
    @property
    def PlayListId(self): return self.pid
    @property
    def PlayListTitle(self): return self.meta.PlayListTitle
    @property
    def VideoIds(self): return self.meta.VideoIds
    @property
    def vids(self): return DataModel('PlaylistVideoMap').distinct('vid', {'pid':self.pid})
    @property
    def MusicTarget(self): return self.Videos.distinct('vid', {'vid':{'$in':[self.vids]}, 'mp3':{'$in':[None,False]}})
    @property
    def VideoTarget(self): return self.Videos.distinct('vid', {'vid':{'$in':[self.vids]}, 'mp4':{'$in':[None,False]}})
    def show_property(self):
        pretty_title(f"프로퍼티 of {self.__class__.__name__}")
        print('Videos-->', self.Videos)
        print('PlayListId:', self.PlayListId)
        print('PlaylistURL-->', self.PlaylistURL)
        print('WatchURL-->', self.WatchURL)
        print('MusicTarget:', self.MusicTarget, len(self.MusicTarget))
        print('VideoTarget:', self.VideoTarget, len(self.VideoTarget))
        if hasattr(self, 'meta'):
            print('PlayListTitle:', self.PlayListTitle)
            print('VideoIds:', self.VideoIds, len(self.VideoIds))

    @ctracer
    def view(self):
        pretty_title(f'플레이리스트 [{self.name}]')
        model = DataModel('PlaylistVideoMap')
        cursor = model.find({'pid':self.pid}, sort=[('idx',ASCENDING)])

        model = self.Videos
        for d in list(cursor):
            vid, idx = d['vid'], d['idx']
            title = model.distinct('smpl_title', {'vid':vid})[0]
            print(f"[{str(idx).zfill(2)}]", title)
    @ctracer
    def select_video(self, title):
        # Video를 선택한다
        for k,v in self.VideoObjects.items():
            m = re.search(title, v.full_title, flags=re.I)
            self.selected = None if m is None else v
            if m is not None: break
        return self
    @ctracer
    def remove_video(self, title):
        # 플레이리스트 상에서만 Video를 제거. Video 자체가 삭제되는 것은 아니다.
        self.select_video(title)
        for k,v in self.VideoObjects.items():
            if k == self.selected._id:
                del self.VideoObjects[k]
        return self
    @ctracer
    def info(self):
        # 플레이리스트 간략정보
        pretty_title('플레이리스트 정보')
        for k,v in self.__dict__.items():
            if k in ['name','url','pid']: print('-',k,v)
    @ctracer
    def download(self):
        # 다운로드 대상 중 마지막 Video 의 다운로드가 끝나면 모든 다운로드가 완료되었다는 시그널을 발생시킨다
        try:
            self.fetch()
            targets = []
            for title, video in self.VideoObjects.items():
                if not hasattr(video, 'mp3'): targets.append(video)
            if len(targets) > 0:
                last_video = targets[-1]
                last_video.download_completed.connect(self.PlaylistDownloadCompleted)
                for video in targets:
                    dbg.dict(video)
                    video.download('mp3')
                    # break
            else:
                logger.info(f'{self} | 다운로드할 대상이 없다')
        except Exception as e:
            logger.error([self, e])
            raise
    @ctracer
    def PlaylistDownloadCompleted(self): pass

# 하나의 플레이리스트 안의 비디오들 메타정보
class PlaylistMeta:

    def __init__(self, url):
        # 구글계정없이 액세스할 수 있는 'WatchURL'을 사용해야한다
        self.res = requests.get(url)
        self._parse(self.res.text)
    def _parse(self, html):
        # SectionGubun('HTML파싱')
        soup = BeautifulSoup(html, 'html.parser')
        s = soup.find('script', string=re.compile('var ytInitialData'))

        txt = s.get_text().strip()
        txt = re.sub('^var ytInitialData = ', repl='', string=txt)
        txt = re.sub(';$', repl='', string=txt)
        txt = re.sub('\s+', repl=' ', string=txt)

        d = json.loads(txt)
        # for k,v in d.items(): setattr(self, k, v)

        # 핵심정보
        try:
            self._playlist = d['contents']['twoColumnWatchNextResults']['playlist']['playlist']
        except Exception as e:
            logger.error([self, e])
            raise
        else:
            self._parse_contents()
    def _parse_contents(self):
        data = []
        for con in self._playlist['contents']:
            try:
                data.append(con['playlistPanelVideoRenderer'])
            except Exception as e:
                logger.error([self, e])

        df = pd.json_normalize(data)
        _nameMap = {
            'title.simpleText':'smpl_title',
            'title.accessibility.accessibilityData.label':'full_title'
        }
        df = df.rename(columns=_nameMap)
        df = df.reset_index()
        self._contents = df.to_dict('records')
    @property
    def PlayListId(self): return self._playlist['playlistId']
    @property
    def PlayListTitle(self): return self._playlist['title']
    @property
    def VideoIds(self): return list(pd.DataFrame(self._contents)['videoId'])
    def show_property(self):
        pp.pprint(self.PlayListId)
        pp.pprint(self.PlayListTitle)
        pp.pprint(self.VideoIds)


class VideoMeta:
    def __init__(self, vid):
        self.vid = vid
        self.url = f'https://youtu.be/{self.vid}'
    @ctracer
    def fetch(self): pass


class Video(BaseQWorker):
    download_completed = pyqtSignal()

    @ctracer
    def __init__(self, filter):
        super().__init__()
        self.identify(filter)
        self.download_completed.connect(self.update_extraInfo)
        self.fhandler = FileHandler()
        self.y2mate = Y2MateBrowser(self.url)
        self.y2mate.finished.connect(self.close)
        # 다운로드경로 자동셋팅
        self.set_dlpath(None)
        self.set_filename(self.smpl_title)
        # dbg.dict(self.fhandler)
        # dbg.dict(self.y2mate)
        self.workers = {}

    @property
    def Videos(self): return DataModel('Videos')
    @property
    def PlaylistVideoMap(self): return DataModel('PlaylistVideoMap')
    @ctracer
    def identify(self, filter):
        try:
            cursor = self.Videos.find(filter, limit=1)
            for k,v in list(cursor)[0].items(): setattr(self, k, v)
            self.url = f'https://youtu.be/{self.vid}'
        except Exception as e:
            logger.error([self, e])
            raise
    @ctracer
    def set_dlpath(self, path):
        self.fhandler.set_dlpath(path)
        self.y2mate.set_dlpath(self.fhandler.dl_path)
    @ctracer
    def set_filename(self, filename):
        self.fhandler.set_filename(filename)
        self.y2mate.set_filename(self.fhandler.filename)
    @ctracer
    def download(self, ftype='mp3', fquality=None):
        try:
            if ftype in ['mp3','mp4']:
                self.target = DataClass()
                self.target.ftype = ftype
                self.target.fquality = fquality
                funcName = f'get_{ftype}'
                if fquality is not None: self.y2mate.set_fquality(fquality)
                worker = WorkerGenerator(self.y2mate, func=funcName)
                worker.finished.connect(self.download_completed.emit)
                self.workers.update({ftype: worker})
                PartGubun(f'스레드 시작--> {[self.fhandler.filename]}')
                worker.start()
            else:
                logger.error(f"{self} | y2mate 에서는 FileType: [mp3|mp4]만 지원한다")
        except Exception as e:
            logger.error([self, e])
            raise
    @ctracer
    def update_extraInfo(self):
        d = {'filename':self.fhandler.filename, self.target.ftype:True}
        self.Videos.update_one({'vid':self.vid}, {'$set':d})

    @ctracer
    def open_youtube(self):
        if hasattr(self, 'url'): pass
