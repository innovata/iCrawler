import os 
import sys 
from importlib import reload


import requests



# 프로젝트 소스코드 위치 셋업
_dir = os.path.join('c:\pypjts', 'iCrawler', 'src')
sys.path.append(_dir)



from ipycrawl import file, linkedin, saramin



def reload_all():
    modules = [
        file, linkedin, saramin
    ]
    for m in modules: reload(m)