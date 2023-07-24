# -*- coding: utf-8 -*-
import os 
from urllib.parse import urlparse, urlunparse
import json 
import re 
from datetime import datetime
from time import sleep


import requests
import pandas as pd
from bs4 import BeautifulSoup


from ipylib.idebug import *
from ipylib import idatetime


from ipycrawl import credential




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


def saramin_secret(): return credential.read_credential_file('사람인')


def access_key():
    d = saramin_secret()
    return d['ACCESS_KEY']

def id_passward():
    d = saramin_secret()
    return d['USER_ID'], d['USER_PASSWORD']


def get_id_from_url(url):
    o = urlparse(url)
    for e in o.query.split('&'):
        k, v = e.split('=')
        if k == 'rec_idx': return v        



################################################################
"""OpenAPI"""
################################################################


"""사람인 OpenAPI"""
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
    
    DESCRIPTION = """
        API Documentation: https://oapi.saramin.co.kr/guide/job-search-id
        id를 특정하지 않을 경우 기본값으로 최대 110개씩 응답한다
    """
    print(DESCRIPTION.strip())

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
    
    dic = json.loads(r.text)
    # print({'list(dic)': list(dic)})
    if 'jobs' in dic:
        d = dic['jobs'].copy()
        del d['job']
        logger.info(d)
        return dic
    else:
        logger.error(dic)
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


"""사람인 코드표(직무/직업) 수집"""
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


class OpenAPI(object):

    def __init__(self): pass
    def jobsearch(self, **kwargs): return JobSearchAPI(**kwargs)
    def get_data(self, js): return get_data(js)
    def collect_codeTables(self): return collect_codeTables()



################################################################
"""Selenium"""
################################################################

HOME_URL = 'https://www.saramin.co.kr/'



from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


from ipycrawl import seleniumX 



class SaramInBrowser(object):

    def __init__(self):
        self.driver = seleniumX.get_driver()
        self.driver.get(HOME_URL)

    def login(self): login(self.driver)
    """채용공고 페이지이동"""
    def goto_jobPost(self, url): goto_jobPost(self.driver, url) 
    """기업정보 페이지이동"""
    def goto_companyInfoPage(self, csn): goto_companyInfoPage(self.driver, csn)
    """기업연봉 페이지이동"""
    def goto_companySalaryPage(self, csn): goto_companySalaryPage(self.driver, csn)


def login(driver):
    driver.get('https://www.saramin.co.kr/zf_user/auth')
    id, pw = id_passward()
    
    input_id = driver.find_element(By.ID, 'id')
    # print({'input_id': input_id})
    input_pw = driver.find_element(By.ID, 'password')
    # print({'input_pw': input_pw})
    seleniumX.fill_inputBox(driver, input_id, id, wait=1)
    seleniumX.fill_inputBox(driver, input_pw, pw, wait=1)
    seleniumX.press_enter(driver)


def goto_jobPost(driver, url):
    rec_idx = get_id_from_url(url)
    print({'rec_idx': rec_idx})
    driver.get(url)
    print({'current_url': driver.current_url})


def goto_companyInfoPage(driver, csn):
    url = 'https://www.saramin.co.kr/zf_user/company-info/view'
    url = f'{url}?csn={csn}'
    driver.get(url)


def goto_companySalaryPage(driver, csn):
    url = 'https://www.saramin.co.kr/zf_user/salaries/total-salary/view'
    url = f'{url}?csn={csn}'
    driver.get(url)





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
        self._setup_csn()
    
    # 관심기업등록 버튼으로부터 csn 값 찾아내서 셋업
    def _setup_csn(self):
        btn = self._get_btn()
        button = btn.find('button', attrs={'title': '관심기업 등록'})
        # print(button.prettify())
        # pp.pprint(button.attrs)
        self.csn = button.attrs['csn']

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
    def goto_companySalaryPage(self):
        btn = self._get_btn()
        a = btn.find('a', attrs={'href': re.compile('total-salary')})
        if a is None:
            # print({'a': a})
            logger.warning(['연봉정보 없음', {'atag': a}])
        else:
            # print(a.prettify())
            url = self.homeUrl + a.attrs['href']
            # print(url)
            self.driver.get(url)
    # 기업정보 페이지로 이동
    def goto_companyInfoPage(self): 
        btn = self._get_btn()
        a = btn.find('a', attrs={'href': re.compile('company-info')})
        if a is None:
            # print({'a': a})
            logger.warning(['기업정보 없음', {'atag': a}])
        else:
            # print(a.prettify())
            url = self.homeUrl + a.attrs['href']
            # print(url)
            self.driver.get(url)
    

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


def parse_integer(s):
    v = s.strip().replace(',', '')
    return int(v)


def parse_salary_in_tag(tag):
    s = tag.get_text()
    # print({'text': s})
    m = re.search('([0-9,]+)\s*([가-힣]+)', s)
    if m is None:
        logger.warning(['정보없음', {'match': m, 'text': s}, tag.prettify()])
    else:
        # print([m[1], m[2]])
        v1 = parse_integer(m[1])
        _map = {
            '만원': pow(10, 4)
        }
        v2 = _map[m[2]]
        return v1 * v2


def parse_money_n_unit(s):
    _map = {
        '만원': pow(10, 4),
        '억': pow(10, 8),
    }
    li = re.findall('([\d,]+)\s*([가-힣]*)', s)
    # print(li)
    _sum = 0
    for n, unit in li:
        v = parse_integer(n)
        unit = _map[unit]
        _sum += v * unit
    return _sum 


def get_company_data(driver, csn):
    goto_companyInfoPage(driver, csn)
    d1 = CompanyIntroPage(driver).parse()
    pp.pprint(d1)

    goto_companySalaryPage(driver, csn)
    sleep(1)
    d2 = CompanySalaryPage(driver).parse()
    d1.update(d2)
    return d1


"""개별 기업 연봉정보 상세 페이지"""
class CompanySalaryPage(object):
    # 로그인해야 상세정보를 알 수 있다

    def __init__(self, driver):
        self.driver = driver 
        self.orgUrl = driver.current_url
    """필요한 모든 데이터 파싱"""
    def parse(self):
        d = {
            '평균연봉': self.avg_salary(),
            '최저연봉': self.min_salary(),
            '최고연봉': self.max_salary(),
            '연봉정보-신뢰도': self.salary_info_reliability(),
            '대졸초임': self.fresh_man_salary(),
            '직급별연봉': self.cascade_salary(),
        }
        return d
    """평균연봉"""
    def avg_salary(self): 
        soup = get_soup(self.driver)
        div = soup.find('div', id='tab_avg_salary')
        p = div.find('p', class_='average_currency')
        if p is None:
            logger.warning(['평균연봉 정보없음', div.prettify()])
        else:
            # print(p.prettify())
            return parse_salary_in_tag(p)
    """최저연봉"""
    def min_salary(self):
        soup = get_soup(self.driver)
        div = soup.find('div', id='tab_avg_salary')
        div = div.find('div', class_='aver_bar')
        span = div.find('span', class_='min_txt')
        if span is None:
            logger.warning(['최저연봉 정보없음', div.prettify()])
        else:
            return parse_salary_in_tag(span)
    """최고연봉"""
    def max_salary(self): 
        soup = get_soup(self.driver)
        div = soup.find('div', id='tab_avg_salary')
        div = div.find('div', class_='aver_bar')
        span = div.find('span', class_='max_txt')
        if span is None:
            logger.warning(['최고연봉 정보없음', div.prettify()])
        else:
            return parse_salary_in_tag(span)
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
    def estimated_salary(self): pass
    """대졸초임"""
    def fresh_man_salary(self): 
        soup = get_soup(self.driver)
        h2 = soup.find('h2', id='tab_univ_salary')
        div = h2.parent
        # print(div.prettify())
        p = div.find('p', class_=re.compile('^salary$'))
        return parse_salary_in_tag(p)
    """직급별 연봉"""
    def cascade_salary(self): 
        soup = get_soup(self.driver)
        
        # 컬럼명 추출
        div = soup.find('div', id='rank_run')
        # columns = div.find('div', class_='head_list_range')

        # 테이블 데이터
        div = soup.find('div', id='positon_list_div')
        dls = div.find_all('dl')
        data = []
        for dl in dls:
            position = dl.find('dt', class_='title')
            position = position.get_text().strip()
            avg_sal = dl.find('dd', class_='index')
            avg_sal = parse_integer(avg_sal.get_text()) * pow(10, 4)
            # print([position, avg_sal])
            data.append({'직급': position, '평균연봉': avg_sal})
        return data
    """연령별 연봉"""
    def age_salary(self): 
        soup = get_soup(self.driver)
        # h2 = soup.find('div', id='tab_age_salary')
        # div = h2.parent

        # 선그래프 영역
        div = soup.find('div', id='linechart_area')


"""개별 기업소개 상세 페이지"""
class CompanyIntroPage(object):

    def __init__(self, driver):
        self.driver = driver 

    def parse(self):
        설립일자, 업력 = self.publish_date()
        d = {
            '설립일자': 설립일자,
            '업력': 업력,
            '기업형태': self.company_size(),
            '사원수': self.n_employees(),
            '매출액': self.revenue(),
            '업종': self.upjong(),
            '대표자명': self.CEO_name(),
            '홈페이지': self.homepage(),
            '기업주소': self.address(),
            '기업비전': self.vision(),
            '직원수변화': self.trend_of_n_employees(),
        }
        return d 
    """기업개요 표"""
    def _get_summary(self, n=0):
        soup = get_soup(self.driver)
        div = soup.find('div', class_='box_company_view company_intro')
        ul = div.find('ul', class_=re.compile('^summary$'))
        # print(ul.prettify())
        uls = ul.find_all('li')
        return uls[n]
    """업력, 설립일자"""
    def publish_date(self):
        li = self._get_summary(0)
        설립일자 = li.find('span').get_text().strip()
        업력 = li.find('strong').get_text().strip()
        m = re.search('(^\d+년\s\d+월\s\d+일).+', 설립일자)
        dt = datetime.strptime(m[1], '%Y년 %m월 %d일')
        m = re.search('(\d+년차)', 업력)
        return dt, m[1]
    """기업형태"""
    def company_size(self):
        li = self._get_summary(1)
        botton = li.find('button', class_='btn_company_scale')
        return botton.get_text().strip()
    """사원수"""
    def n_employees(self):
        li = self._get_summary(2)
        text = li.find('strong').get_text().strip()
        m = re.search('(\d+)명', text)
        return int(m[1])
    """매출액"""
    def revenue(self):
        li = self._get_summary(3)
        text = li.find('strong').get_text().strip()
        return parse_money_n_unit(text)
    """기업개요 리스트 형태"""
    def _get_info_tag(self):
        soup = get_soup(self.driver)
        return soup.find('dl', class_=re.compile('^info$'))
    """업종"""
    def upjong(self):
        dl = self._get_info_tag()
        dt = dl.find('dt', string='업종')
        dd = dt.find_next_sibling('dd')
        return dd.get_text().strip()
    """대표자명"""
    def CEO_name(self):
        dl = self._get_info_tag()
        dt = dl.find('dt', string='대표자명')
        dd = dt.find_next_sibling('dd')
        return dd.get_text().strip()
    """홈페이지"""
    def homepage(self):
        dl = self._get_info_tag()
        dt = dl.find('dt', string='홈페이지')
        dd = dt.find_next_sibling('dd')
        return dd.a.attrs['href']
    """기업주소"""
    def address(self):
        dl = self._get_info_tag()
        dt = dl.find('dt', string='기업주소')
        dd = dt.find_next_sibling('dd')
        text = dd.get_text().strip()
        return re.sub('\s*지도보기', repl='', string=text)
    """기업비전"""
    def vision(self):
        dl = self._get_info_tag()
        soup = get_soup(self.driver)
        dl = soup.find('dl', class_='info vision gradient')
        dt = dl.find('dt', string='기업비전')
        dd = dt.find_next_sibling('dd')
        return dd.get_text().strip()
    """직원 수 변화"""
    def trend_of_n_employees(self):
        soup = get_soup(self.driver)
        div = soup.find('div', id='employee_graph_info')
        divs = div.find_all('div', class_='wrap_graph')
        data = []
        for d in divs:
            text = d.em.get_text()
            dt = datetime.strptime(text, '%Y.%m')
            num = d.find('span', class_='txt_value').get_text().strip()
            data.append({
                '연월': text,
                '직원수': int(num),
            })
        return data
    

