# -*- coding: utf-8 -*-
import os 
from urllib.parse import urlparse
import json 
import re 
from datetime import datetime


import requests
import pandas as pd
from bs4 import BeautifulSoup


from ipylib.idebug import *
from ipylib import idatetime





def get_access_key():
    try:
        return os.environ['SARAMIN_KEY']
    except Exception as e:
        logger.error([e, "os.environ['SARAMIN_KEY']=YOUR_ACCESS_KEY"])
        raise

ACCESS_KEY = get_access_key()


DICTIONARY = {
    'opening-timestamp': '채용공고 시작일',
    'modification-timestamp': '채용공고 수정일',
    'posting-date': '최초작성일',
    'expiration-date': '채용공고 종료일',
    'apply-cnt': '지원자수',
    'read-cnt': '조회수',
    # '': '',
    # '': '',
    # '': '',
}



def get_id_from_url(url):
    o = urlparse(url)
    for e in o.query.split('&'):
        k, v = e.split('=')
        if k == 'rec_idx': return v        


"""id를 특정하지 않을 경우 기본 10개씩 응답한다"""
def JobSearchAPI(
        id=None,
        keywords=None,
        bbs_gb=None,
        stock=None,
        sr=None,
        loc_cd=None,
        published=None,
        fields='posting-date,expiration-date,keyword-code,count',
        deadline=None,
        start=0,
        count=110,
        sort='pd'):
    
    uri = 'https://oapi.saramin.co.kr/job-search'

    params = {
        'access-key': ACCESS_KEY,
        'id': id,
        'keywords': _handle_keywords(keywords),
        'bbs_bg': bbs_gb,
        'stock': stock,
        'sr': sr,
        'loc_cd': loc_cd,
        'published': published,
        'fields': fields,
        'deadline': deadline,
        'start': start,
        'count': count,
        'sort': sort,
    }
    pp.pprint(params)
    headers = {'Accept': 'application/json'}
    r = requests.get(uri, params=params, headers=headers)
    
    js = json.loads(r.text)
    # print({'list(json)': list(js)})
    if 'jobs' in js:
        d = js['jobs'].copy()
        del d['job']
        logger.info(d)
        return js
    else:
        logger.error(js)
        dbg.dict(r)


def _handle_keywords(v):
    if v is None: return v 
    else: return re.sub('\s', repl='+', string=v)


def get_data(js):
    data = js['jobs']['job']
    if len(data) == 0:
        logger.warning('데이터없음')
    else:
        for d in data:
            # print('-'*100)
            for k, v in d.items():
                _v = ValueParser(k, v)
                # print([k, _v])
                d.update({k: _v})
            # pp.pprint(d)
            # break
    # return data
    return pd.DataFrame(data)
    return pd.json_normalize(data, 'position')


def DatetimeParser(v):
    # return idatetime.DatetimeParser(v)
    if isinstance(v, datetime): 
        return v
    else:
        try:
            return datetime.strptime(v, '%Y-%m-%dT%H:%M:%S%z').astimezone()
        except Exception as e:
            if re.search('\d{10}', v) is not None:
                return datetime.fromtimestamp(int(v)).astimezone()
            else:
                logger.error([e, v])


def ValueParser(k, v):
    # print([k, v])
    if k in ['read-cnt', 'apply-cnt']:
        return int(v)
    elif re.search('timestamp$|date$', k) is not None:
        # print([k, v])
        return DatetimeParser(v)
    else:
        return v
    


"""사람인 코드표 수집"""
def __collect_codeTables__(type='1'):
    url = f'https://oapi.saramin.co.kr/guide/code-table{type}'
    dfs = pd.read_html(url)
    # print(len(dfs))
    return dfs


def __collect_codeTables05__():
    url = 'https://oapi.saramin.co.kr/guide/code-table5'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', class_='apidoc')
    # print(div.prettify())
    if div is None:
        raise 
    else:
        atags = div.find_all('a', attrs={'href': re.compile('code-table')})
        print(len(atags))
        doc = {}
        for a in atags:
            table_name = a.get_text().strip()
            table_name = table_name.replace('·', '/')
            path = a.attrs['href']
            _url = 'https://oapi.saramin.co.kr' + path
            dfs = pd.read_html(_url)
            # print(len(dfs))
            if len(dfs) == 1:
                doc.update({table_name: dfs[0]})
            else: 
                raise
        return doc


"""사람인 코드표 수집"""
def collect_codeTables():
    types = {
        '1': '근무형태/학력/연봉 코드표',
        '2': '근무지/지역 코드표',
        '3': '산업/업종 코드표',
        '5': '직무/직업 코드표',
    }
    doc = {}
    for type in list(types):
        if type == '5':
            d = __collect_codeTables05__()
            doc.update(d)
        else:
            dfs = __collect_codeTables__(type)
            if type == '1':
                doc.update({
                    '근무형태': dfs[0],
                    '학력': dfs[1],
                    '연봉범위': dfs[2],
                })
            elif type == '2':
                doc.update({
                    '사람인 근무지/지역': dfs[0],
                    '2차 근무지/지역': dfs[1],
                    '1차 근무지/지역': dfs[2],
                })
            elif type == '3':
                doc.update({
                    '상위 산업/업종': dfs[0],
                    '산업/업종': dfs[1],
                    '업종 키워드': dfs[2],
                })
    return doc



