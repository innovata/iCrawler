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
    print('\nMedia Info 파싱 후-->')
    pp.pprint(d)

    with open(jsonfile, 'w') as f:
        f.write(json.dumps(d, indent=4))
        f.close()

    print('미디어정보 저장-->', jsonfile)
    return d 


def _get_media_info(url):
    print('\nFetching media_info...')
    pk = CLIENT.media_pk_from_url(url)
    info = CLIENT.media_info(pk)
    # print('\n\n')
    # pp.pprint(info)
    return info 


def _create_media_dir(info, ctype='video'):
    # print(info.user.username)
    video_dir = os.path.join(DOWNLOAD_PATH, f'{ctype}s')
    user_dir = os.path.join(video_dir, info.user.username)
    contents_dir = os.path.join(user_dir, str(info.pk))
    os.makedirs(contents_dir, exist_ok=True)
    return contents_dir


def _download_video_file(info, _dir):
    # 비디오 URL 추출/다운로드
    if  isinstance(info.video_url, HttpUrl):
        urls = [str(info.video_url)]
    elif len(info.resources) > 0:
        urls = [res.video_url for res in info.resources]
    # pp.pprint(urls)
    
    # 파일다운로드
    for i, url in enumerate(urls, start=1):
        srcfile = CLIENT.video_download_by_url(url, folder=_dir)
        # print(srcfile)
        sleep(1)
        dstfile = os.path.join(_dir, str(i).zfill(2)+'.mp4')
        # print(dstfile)
        try:
            os.rename(srcfile, dstfile)
        except FileExistsError as e:
            print('ERROR |', e)
            os.remove(srcfile)

    # 영상 합치기
    return 


def _download_image_file(info, _dir):
    print('info.pk-->', info.pk, type(info.pk))
    srcfile = CLIENT.photo_download(int(info.pk), folder=_dir)

    # CLIENT.photo
    print(srcfile)
    return 


def _download_media(info, ctype='video'):
    # 미디어 디렉토리 생성
    contents_dir = _create_media_dir(info, ctype)

    # 미디어정보 저장
    jsonfile = os.path.join(contents_dir, 'info.json')
    save_media_info(jsonfile, info)
    
    # 파일다운로드
    if ctype == 'video':
        _download_video_file(info, contents_dir)
    elif ctype == 'image':
        _download_image_file(info, contents_dir)
    else:
        print("ERROR | Unknown media type-->", ctype)
    return

 
 
################################################################################
# APIs
################################################################################

def login(username='gabriele'):
    d = credential.read_credientials(CREDENTIAL_PATH)
    cred = d[username]
    print('\n로그인계정-->', cred)
    
    _dir = os.path.dirname(__file__)
    _dir = os.path.join(_dir, '__temp__')
    os.makedirs(_dir, exist_ok=True)
    sess_file = os.path.join(_dir, f"insta_session_{username}.json")

    if os.path.exists(sess_file):
        print("\n기존세션정보 로딩-->", sess_file)
        session = CLIENT.load_settings(sess_file)
        CLIENT.set_settings(session)
    else:
        print("저장된 세션정보 없음.")
        session = None

    try:
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


    CLIENT.dump_settings(sess_file)
    print("\n세션정보 저장-->", sess_file)


def download_video(url):
    info = _get_media_info(url)
    _download_media(info, 'video')
    print('DONE.')


def download_image(url):
    info = _get_media_info(url)
    _download_media(info, 'image')
    print('DONE.')


def get_medias_of_collection(media):
    pk = CLIENT.collection_pk_by_name(media.name)
    print('\nPK-->', pk)
    return CLIENT.collection_medias(pk)


def download_collection_medias(name='All posts'):
    coll_pk = CLIENT.collection_pk_by_name(name)
    print('\nCollection PK-->', coll_pk)
    medias = CLIENT.collection_medias(coll_pk)
    print('\nCollection Medias-->', len(medias))
    for media in medias[:1]:
        try:
            print([media.pk, len(dict(media)), list(dict(media))])
            pp.pprint(media.dict())
            
            info = CLIENT.media_info(media.pk)
            _download_media(info, 'video')
        except Exception as e:
            print('\nERROR |', e)











