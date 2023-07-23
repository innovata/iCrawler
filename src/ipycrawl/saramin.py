# -*- coding: utf-8 -*-
import os 
from urllib.parse import urlparse, urlunparse
import json 
import re 
from datetime import datetime


import requests
import pandas as pd
from bs4 import BeautifulSoup


from ipylib.idebug import *
from ipylib import idatetime








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


def access_key():
    try:
        filepath = os.environ['SARAMIN_CREDENTIAL_PATH']
        if os.path.isfile(filepath): pass 
        else: raise
    except Exception as e:
        logger.error([e, 'README.md 를 읽어보세요'])
        raise
    else:
        with open(filepath, mode='r') as f:
            d = json.loads(f.read())
            f.close()
        return d['ACCESS_KEY']
    

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
        'access-key': access_key(),
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
    return data
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






"""Selenium"""

from selenium import webdriver

def get_driver():
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    pp.pprint(options.__dict__)
    driver = webdriver.Edge(options=options)
    pp.pprint(driver.__dict__)
    return driver



class SeleniumBrowser(object):

    def __init__(self):
        self.driver = get_driver()

    """채용공고 상세페이지"""
    def go_to_posting(self, url): go_to_posting(self.driver, url) 
    def parse_page(self, soup): pass 



def go_to_posting(driver, url):
    rec_idx = get_id_from_url(url)
    print({'rec_idx': rec_idx})
    driver.get(url)
    print({'current_url': driver.current_url})


def parse_page(driver):
    o = urlparse(driver.current_url)
    print(o)
    uri = o.netloc

    rec_idx = get_id_from_url(driver.current_url)
    print({'rec_idx': rec_idx})

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # print({'soup': soup})
    # print(soup.prettify())
    print({'soup': soup.find('title')})
    
    title = soup.find('h1', class_='tit_job')
    print({'tit_job': title})
    
    # s = soup.find('div', attrs={'data-rec_idx': rec_idx})
    # print({'s': s})
    # print(s.prettify())


    btn = soup.find('div', class_='area_notice_btn')
    print({'btn': btn})
    print(btn.prettify())

    a = btn.find('a', attrs={'href': re.compile('total-salary')})
    print({'a': a})
    print(a.prettify())

    url = uri + a.attrs['href']
    url = o.scheme +'://'+ o.netloc + a.attrs['href']
    print(url)


    # atags = soup.find_all('a')
    # for a in atags:
    #     text = a.get_text().strip()
    #     if len(text) > 0: print(text)
    return 


def home_url(driver):
    o = urlparse(driver.current_url)
    return o.scheme +'://'+ o.netloc


def get_soup(driver):
    html = driver.page_source
    return BeautifulSoup(html, 'html.parser')



"""개별 채용공고 상세 페이지"""
class JobPostPage(object):

    def __init__(self, driver):
        self.driver = driver
        self.homeUrl = home_url(driver)
        self.orgUrl = driver.current_url
        self.rec_idx = get_id_from_url(driver.current_url)
    
    def refresh(self): self.driver.get(self.orgUrl)

    def parse(self): 
        # 채용공고 직무 타이틀 셋업
        soup = get_soup(self.driver)
        title = soup.find('h1', class_='tit_job')
        print({'tit_job': title})
        self.jobTitle = title.get_text().strip()

        self._setup_csn()

        pp.pprint(self.__dict__)

    def _get_btn(self):
        soup = get_soup(self.driver)
        btn = soup.find('div', class_='area_notice_btn')
        # print({'btn': btn})
        # print(btn.prettify())
        return btn
    # 연봉정보 페이지로 이동
    def goto_salary_page(self):
        btn = self._get_btn()
        a = btn.find('a', attrs={'href': re.compile('total-salary')})
        # print({'a': a})
        # print(a.prettify())

        url = self.homeUrl + a.attrs['href']
        # print(url)
        self.driver.get(url)

    # 기업정보 페이지로 이동
    def goto_companyInfo_page(self): 
        btn = self._get_btn()
        a = btn.find('a', attrs={'href': re.compile('company-info')})
        # print({'a': a})
        # print(a.prettify())

        url = self.homeUrl + a.attrs['href']
        # print(url)
        self.driver.get(url)

    # 관심기업등록 버튼으로부터 csn 값 찾아내서 셋업
    def _setup_csn(self):
        btn = self._get_btn()
        button = btn.find('button', attrs={'title': '관심기업 등록'})
        # print(button.prettify())
        # pp.pprint(button.attrs)
        self.csn = button.attrs['csn']


"""개별 기업 연봉정보 상세 페이지"""
class CompanySalaryPage(object):
    # 로그인해야 상세정보를 알 수 있다

    def __init__(self, driver):
        self.driver = driver 
        self.orgUrl = driver.current_url

    def parse(self):
        pass 
    """평균연봉"""
    def avg_salary(self): 
        soup = get_soup(self.driver)
        try:
            div = soup.find('div', id='tab_avg_salary')
            # print(div.prettify())
            
            p = div.find('p', class_='average_currency')
            # print(p.prettify())

            v = p.em.get_text().strip().replace(',', '')
            # print(int(v))
            return int(v)
        except Exception as e:
            logger.error(e)
    """최저연봉"""
    def min_salary(self):
        soup = get_soup(self.driver)
        try:
            div = soup.find('div', id='tab_avg_salary')
            div = div.find('div', class_='aver_bar')
            span = div.find('span', class_='min_txt')
            v = span.em.get_text().strip().replace(',', '')
            return int(v)
        except Exception as e:
            logger.error(e)
    """최고연봉"""
    def max_salary(self): 
        soup = get_soup(self.driver)
        try:
            div = soup.find('div', id='tab_avg_salary')
            div = div.find('div', class_='aver_bar')
            span = div.find('span', class_='max_txt')
            v = span.em.get_text().strip().replace(',', '')
            return int(v)
        except Exception as e:
            logger.error(e)
    """연봉정보 신뢰도"""
    def salary_info_reliability(self):
        soup = get_soup(self.driver)
        try:
            div = soup.find('div', id='tab_avg_salary')
            div = div.find('div', class_='textinfo')
            dd = div.find('dd', class_='reliability')
            return dd.get_text().strip()
        except Exception as e:
            logger.error(e)
    """맞춤 연봉정보"""
    def _estimated_salary(self): pass
    """대졸초임"""
    def _fresh_man_salary(self): pass
    """직급별 연봉"""
    def _fresh_man_salary(self): pass
    """연령별 연봉"""
    def _fresh_man_salary(self): pass


"""개별 기업소개 상세 페이지"""
class CompanyIntroPage(object):

    def __init__(self, driver):
        self.driver = driver 

    def parse(self):
        # 회사 홈페이지 URL
        # 회사 주소

        pass 
    """직원 수 데이터 셋업"""
    def _setup_n_employees(self):
        self.employeesNumData
