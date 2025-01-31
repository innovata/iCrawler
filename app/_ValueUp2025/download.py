# -*- coding: utf-8 -*-


import re 
import os 


import requests





def download_stream(url, outfile):

    def _next_url(url):
        m = re.search(r'_(\d+)\.ts$', url) 
        # print("Match-->", m)
        if m is None:
            print("ERROR | URL 오류-->", url)
            return None 
        else:
            # print("SEQ-->", m.group(1))
            seq = int(m.group(1)) + 1
            _url = re.sub(r'_(\d+)\.ts$', repl=f'_{seq}.ts', string=url) 
            # print('Next URL-->', _url)
        return _url 

    # return 

    with open(outfile, 'wb') as f:
        while True:
            print("URL-->", url)
            res = requests.get(url, stream=True)
            print("Response code-->", res.status_code)

            if res.status_code == 200:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

                url = _next_url(url)
                if url is None:
                    break 
                else:
                    pass 
            else:
                print('루프 종료.')
                break 

        f.close()
    
    print(f'다운로드 완료-->', outfile)

title = "Virtuous Datacenters with QUANTA Computers"
outfile = f"D:\\WORK_DRIVE\\VALUE UP 2025\\{title}.mp4"
# url = "https://cn.hlscache.vodalys.io/vod/_definst_/0/Y/x/0YxzrySfWpu3dBAK.mp4/media_w971825470_0.ts"

title = "Virtuous Datacenters with QUANTA Computers"
outfile = f"D:\\WORK_DRIVE\\VALUE UP 2025\\{title}.mp4"
url = "https://cn.hlscache.vodalys.io/vod/_definst_/d/O/y/dOyGEIKQhYiqCcbX.mp4/media_w2046179807_0.ts"


title = "Productization Revolution (Simplify collaboration at any scale and onboard on construction industrialization)"
outfile = f"D:\\WORK_DRIVE\\VALUE UP 2025\\{title}.mp4"
url = "https://cn.hlscache.vodalys.io/vod/_definst_/v/6/N/v6Nkbj1YdsP6w6i1.mp4/media_w580015331_0.ts"


title = "How does DASSAULT SYSTÈMES shape the future of automotive"
outfile = f"D:\\WORK_DRIVE\\VALUE UP 2025\\{title}.mp4"
url = "https://cn.hlscache.vodalys.io/vod/_definst_/y/v/Q/yvQFXr7xudfYvCX6.mp4/media_w1530844141_0.ts"



download_stream(url, outfile)











