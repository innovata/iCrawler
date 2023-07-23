# -*- coding: utf-8 -*-
import os 
from urllib.parse import urlparse


import requests


from ipylib.idebug import *



def req():
    url = 'https://www.linkedin.com/oauth/v2/accessToken'
    params = {
        'grant_type': 'client_credentials',
        'client_id': '862e6tc8af5xjk',
        'client_secret': 'ZtOedplnouwwnMZ3'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = requests.request('POST', url, data=params, headers=headers)
    print(res)
    pp.pprint(res.__dict__)
    pp.pprint(res.headers)
    print(res.text)
