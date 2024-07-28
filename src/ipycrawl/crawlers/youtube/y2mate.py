# -*- coding: utf-8 -*-
# https://y2mate.com/ 웹사이트에서 마치 사람이 클릭하듯이 움직이는 크롤러.




from urllib.parse import urlparse, parse_qs
import json
import re
import os
from pathlib import PureWindowsPath, PurePosixPath

import requests
from bs4 import BeautifulSoup
import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal

from ipylib.idebug import *
from ipylib import ipath

# from youtube.Lib import *


__all__ = [
    'Y2MateClient',
]











class Y2MateClient(QObject):
    searched = pyqtSignal()
    converted = pyqtSignal()
    ajax_done = pyqtSignal()
    selected = pyqtSignal()

    @tracer.info
    def __init__(self, url):
        super().__init__()

        # 유투브 영상 URL
        self.url = url
        self.dl_path = None
        self.filename = None
        self.set_ftype('mp3')
        self.set_fquality(1080)
    
    @property
    def ftype(self): 
        return self._ftype
    
    @property
    def fquality(self): 
        return self._fquality
    
    def set_dlpath(self, p): 
        self._dl_path = p
    
    def set_filename(self, s): 
        self._filename = s
    
    def set_ftype(self, s): 
        self._ftype = s
    
    def set_fquality(self, n): 
        self._fquality = str(n)

    def search(self):
        try:
            # 샘플 예시 포멧을 기반으로 필요한 파라미터를 변경한다
            o = urlparse('https://suggestqueries.google.com/complete/search?jsonp=jQuery340004144273343421623_1635056106020&q=https%3A%2F%2Fyoutu.be%2Fc9h5VloOhCc%3Flist%3DTLPQMjQxMDIwMjEgBM7O0V7Bvg&hl=en&ds=yt&client=youtube&_=1635056106021')
            qs = parse_qs(o.query)
            print(o)
            pp.pprint(qs)
            # https://youtu.be/c9h5VloOhCc
            # https://youtu.be/OSUxrSe5GbI?list=PLP9YOa5MTwu1_PGGFQgSWUoHwhCx4EEqg

            # 입력받은 유투브URL을 qs객체에 업데이트
            param = {k:v[0] for k,v in parse_qs(o.query).items()}
            param.update({'q':self.url})
            # pp.pprint(param)
            print('geturl:', o.geturl())
            r = requests.get(o.geturl(), param)
            # dbg.dict(r)
            # print(r.text, type(r.text))
        except Exception as e:
            logger.error([self, e])
            raise
        else:
            self.searched.emit()

    @tracer.debug
    def ajax(self):
        try:
            url = 'https://www.y2mate.com/mates/en105/analyze/ajax'
            qs = parse_qs('url=https%3A%2F%2Fyoutu.be%2FagnV2YjuzSM%3Flist%3DPLP9YOa5MTwu06to2NmlacATe-zEXHUOTw&q_auto=0&ajax=1')
            # pp.pprint(qs)
            data = {k:v[0] for k,v in qs.items()}
            data.update({'url':self.url})
            r = requests.post(url, data)
            # dbg.dict(r)

            # SectionGubun('Response-Data')
            d = json.loads(r.text)
            # pp.pprint(d)

            # SectionGubun('HTML파싱')
            soup = BeautifulSoup(d['result'], 'html.parser')
            # print(soup.prettify())
            self.AjaxData = DataClass()

            s = soup.find('div', class_='caption text-left')
            self.AjaxData.title = s.b.get_text().strip()
            if self._filename is None: self.set_filename(self.AjaxData.title)

            s = soup.find('div', class_='thumbnail cover')
            self.AjaxData.thumbnailUrl = s.a.img.attrs['src']

            # SectionGubun('contents 추출')
            self.AjaxData.contents = []
            s = soup.find('div', class_='tab-content')
            for id in ['mp4', 'mp3']:
                # SectionGubun('')
                tab = s.find('div', class_='tab-pane', id=id)
                # print(tab.prettify())
                trs = tab.find('table').find('tbody').find_all('tr')
                for tr in trs:
                    # print(tr.prettify())
                    tds = tr.find_all('td')
                    d = {}
                    d['size'] = tds[1].get_text().strip()
                    for k,v in tds[2].a.attrs.items(): d.update({k.replace('-','_'): v})
                    # pp.pprint(d)
                    self.AjaxData.contents.append(d)

            # SectionGubun('input태그 추출')
            self.AjaxData.input = DataClass()
            for k,v in soup.input.attrs.items(): setattr(self.AjaxData.input, k.replace('-','_'), v)
            dbg.dict(self.AjaxData.input)

            # SectionGubun('K-Data 추출')
            s = soup.find('script', attrs={'type':'text/javascript'})
            # print(s.get_text())
            li = s.get_text().split(';')
            li = [e.strip() for e in li if len(e.strip()) > 0]
            self.AjaxData.k_data = DataClass()
            for e in li:
                m = re.search('var\s([a-z_]+)\s=\s"(.+)"', e)
                d.update({m[1]:m[2]})
                setattr(self.AjaxData.k_data, m[1], m[2])
            dbg.dict(self.AjaxData.k_data)

            dbg.dict(self.AjaxData)
            self.KData = d
            self.ajax_done.emit()
        except Exception as e:
            logger.error([self, e])

    @tracer.debug
    def select_content(self, ftype, fquality=None):
        try:
            for c in self.AjaxData.contents:
                if ftype == c['data_ftype']:
                    if fquality is None:
                        break
                    else:
                        if fquality == c['data_fquality']: break
            self.chosen_content = DataClass()
            for k,v in c.items(): setattr(self.chosen_content, k, v)
        except Exception as e:
            logger.error([self, e])
            raise
        else:
            self.selected.emit()

    @tracer.debug
    def xc(self):
        # PartGubun('xc')
        r = requests.get('https://habeglee.net/s9np/xc')
        # dbg.dict(r)
        d = json.loads(r.text)
        # pp.pprint(d)

    @tracer.debug
    def convert(self):
        try:
            qs = parse_qs('type=youtube&_id=5e9b86ec7527f838068b4591&v_id=agnV2YjuzSM&ajax=1&token=&ftype=mp3&fquality=128')
            qs['_id'] = self.AjaxData.k_data.k__id
            qs['v_id'] = self.AjaxData.k_data.k_data_vid
            qs['ftype'] = self.chosen_content.data_ftype
            qs['fquality'] = self.chosen_content.data_fquality
            pp.pprint(qs)
            r = requests.post('https://www.y2mate.com/mates/convert', data=qs)
            # logger.debug(f'{self} | Response-->\n{r.__dict__}')
            # dbg.dict(r)
            d = json.loads(r.text)

            # SectionGubun('HTML파싱')
            soup = BeautifulSoup(d['result'], 'html.parser')
            href = soup.find('a').attrs['href']
            o = urlparse(href)
            print('href-->', o)
            print('query-->')
            pp.pprint(parse_qs(o.query))
            self.down_url = href
        except Exception as e:
            print(f"ERROR | {e}")
        else:
            self.converted.emit()

    @tracer.debug
    def fetch_img(self):
        try:
            filename = f"{self.filename}.jpg"
            self.imgDL = Downloader(filename, self.dl_path)
            self.imgDL.get(self.AjaxData.thumbnailUrl)
        except Exception as e:
            logger.error([self, e])

    @tracer.debug
    def download(self):
        try:
            filename = f"{self.filename}.{self.chosen_content.data_ftype}"
            self.DL = Downloader(filename, self.dl_path)
            self.DL.finished.connect(self.ContentDownloaded)
            self.DL.get(self.down_url)
        except Exception as e:
            logger.error([self, e])

    @tracer.debug
    def browsing(self):
        self.searched.connect(self.ajax)
        self.ajax_done.connect(self.fetch_img)
        self.selected.connect(self.convert)
        self.converted.connect(self.download)
        self.search()
        return self
    
    @tracer.debug
    def get_mp3(self): 
        self.browsing().select_content('mp3')
    
    @tracer.debug
    def get_mp4(self): 
        self.browsing().select_content('mp4', self.fquality)

    @tracer.debug
    def ContentDownloaded(self): 
        self.finished.emit()
