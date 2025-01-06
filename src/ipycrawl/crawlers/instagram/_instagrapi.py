# -*- coding: utf-8 -*-
# Python Package instagrapi 를 이용한 크롤러. 
# pip install instagrapi 
# pip install Pillow



import os 
import json 
import pprint 
pp = pprint.PrettyPrinter(indent=2)
from time import sleep 
from datetime import datetime


from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from pydantic import HttpUrl 


from ipycrawl import credential


CREDENTIAL_PATH = os.environ['INSTAGRAM_CREDENTIAL_PATH']
DOWNLOAD_PATH = os.environ['INSTAGRAM_DOWNLOAD_PATH']



CLIENT = Client()




def login(username='gabriele'):
    d = credential.read_credientials(CREDENTIAL_PATH)
    cred = d[username]
    print('로그인계정-->', cred)
    
    _dir = os.path.dirname(__file__)
    _dir = os.path.join(_dir, '__temp__')
    os.makedirs(_dir, exist_ok=True)
    sess_file = os.path.join(_dir, f"insta_session_{username}.json")

    if os.path.exists(sess_file):
        print("\n기존세션정보 로드-->", sess_file)
        session = CLIENT.load_settings(sess_file)
    else:
        pass 

    if session:
        try:
            CLIENT.set_settings(session)
            v = CLIENT.login(cred['ID'], cred['PASSWORD'])
            print({'로그인결과': v})
            try:
                print('\nChecking session...')
                rv = CLIENT.get_timeline_feed()
                print(['Session Valid-->', type(rv), list(rv), rv['num_results']])
            except LoginRequired:
                print("Session is invalid, need to login via username and password")
        except Exception as e:
            print("Couldn't login user using session information: %s" % e)
    else:
        pass 


    if os.path.exists(sess_file):
        pass 
    else:
        CLIENT.dump_settings(sess_file)
        print("세션정보 임시저장-->", sess_file)



def get_videoUrl(media):
    if getattr(media, 'video_url'): 
        url = media.video_url
    elif len(media.resources) > 0: 
        url = media.resources[0].video_url
    else: 
        raise
    print({'video_url': url})
    return url



def save_media_info(jsonfile, info):
    print('\nSaving media_info...')

    def _handle_httprul(obj):
        if isinstance(obj, HttpUrl):
            obj = str(obj)
        else:
            pass 
        return obj
    
    # d = info.dict() 
    d = {}
    for k,v in info.dict().items():
        if isinstance(v, str) or isinstance(v, int) or isinstance(v, float) or isinstance(v, bool):
            pass 
        elif v is None:
            pass 
        elif isinstance(v, datetime):
            v = v.isoformat()
        elif isinstance(v, dict):
            # for k1,v1 in v.items():
            #     v1 = _handle_httprul(v1)
            v = {'count': len(v)}
        elif isinstance(v, list):
            # for elem in v:
            #     if isinstance(elem, dict):
            #         for k1,v1 in elem.items():
            #             v1 = _handle_httprul(v1)
            #     else:
            #         pass 
            v = [len(v)]
        elif isinstance(v, HttpUrl):
            v = str(v)
        else:
            print(["Unknown type-->", k, v, type(v)])
            v = None
        d.update({k: v})
    
    print('\n\n')
    print('\n데이터 파싱 후-->')
    pp.pprint(d)

    with open(jsonfile, 'w') as f:
        f.write(json.dumps(d, indent=4))
        f.close()

    print('미디어정보 저장-->', jsonfile)
    return d 



def fetch_media_info(url):
    print('\nFetching media_info...')
    pk = CLIENT.media_pk_from_url(url)
    info = CLIENT.media_info(pk)
    # print('\n\n')
    # pp.pprint(info)
    return info 




def download_video(url):
    info = fetch_media_info(url)

    # 디렉토리 생성
    # print(info.user.username)
    video_dir = os.path.join(DOWNLOAD_PATH, 'videos')
    user_dir = os.path.join(video_dir, info.user.username)
    contents_dir = os.path.join(user_dir, str(info.pk))
    os.makedirs(contents_dir, exist_ok=True)


    # 미디어정보 저장
    jsonfile = os.path.join(contents_dir, 'info.json')
    save_media_info(jsonfile, info)


    # 비디오 URL 추출/다운로드
    if  isinstance(info.video_url, HttpUrl):
        urls = [str(info.video_url)]
    elif len(info.resources) > 0:
        urls = [res.video_url for res in info.resources]
    # pp.pprint(urls)
    filenames = []
    for i, url in enumerate(urls, start=1):
        srcfile = CLIENT.video_download_by_url(url, folder=contents_dir)
        # print(srcfile)
        sleep(1)
        dstfile = os.path.join(contents_dir, str(i).zfill(2)+'.mp4')
        # print(dstfile)
        try:
            os.rename(srcfile, dstfile)
        except FileExistsError as e:
            print('ERROR |', e)
            os.remove(srcfile)
        

    # 영상 합치기

    print('DONE.')


def download_image(url):
    info = fetch_media_info(url)

    # 디렉토리 생성
    img_dir = os.path.join(DOWNLOAD_PATH, 'images')
    user_dir = os.path.join(img_dir, info.user.username)
    contents_dir = os.path.join(user_dir, str(info.pk))
    os.makedirs(contents_dir, exist_ok=True)


    # 미디어정보 저장
    jsonfile = os.path.join(contents_dir, 'info.json')
    parsed_info = save_media_info(jsonfile, info)


    srcfile = CLIENT.photo_download_by_url(info.thumbnail_url, folder=contents_dir)
    print(srcfile)


    print('DONE.')



class Media:

    def __init__(self, media):
        super().__init__()
        self.media = media
    def download(self, path=None):
        path = DOWNLOAD_PATH if path is None else path
        video_url = get_videoUrl(self.media)
        CLIENT.video_download_by_url(video_url, folder=path)
