# -*- coding: utf-8 -*-


import os 
from urllib.parse import urlparse
from pathlib import WindowsPath
import pprint
pp = pprint.PrettyPrinter(indent=2)
from time import sleep 


import requests





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


def download_stream(url, filepath):
    # 파일을 바이너리 쓰기 모드로 열기
    with open(filepath, 'wb') as file:
        seq = 0
        while True:
            seq += 1
            _url = url + '/' + f'media_w366098623_{seq}.ts'
            print("URL-->", _url)
            # 스트리밍 모드로 GET 요청
            response = requests.get(_url, stream=True)
            print("Response Code-->", response.status_code)
            
            # 요청이 성공했는지 확인
            if response.status_code == 200:
                file.write(response.content)
                sleep(1)
            else:
                print("루프 종료, 파일 쓰기 완료.")
                file.close()
                break 