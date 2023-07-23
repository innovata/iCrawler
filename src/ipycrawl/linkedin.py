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








# -*- coding: utf-8 -*-
import os 
from datetime import time
from time import sleep
import re 


from ipylib.idebug import *


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains





class LinkedInCollector(object):

    def __init__(self): 
        super().__init__()
        self.driver = webdriver.Chrome()
    def finish(self):
        self.driver.quit()




class LoginAPI(object):

    def __init__(self, driver):
        self.driver = driver

    def login(self, userid, password, site='loginpage'):
        self.userid = userid
        self.password = password

        def __is_logined__():
            return True if self.driver.current_url == 'https://www.linkedin.com/feed/' else False

        if __is_logined__():
            logger.info('이미 로그인된 상태. Move to main-page')
        else:
            logger.info({'로그인 전 URL': self.driver.current_url})
            self._login_onLoginPage()
            logger.info({'로그인 후 URL': self.driver.current_url})
    
    def _login_onLoginPage(self, sleepsecs=1):
        self.driver.get('https://www.linkedin.com/login/')
        sleep(sleepsecs)
        username = self.driver.find_element(By.ID, 'username')
        username.clear()
        username.send_keys(self.userid)

        sleep(sleepsecs)
        password = self.driver.find_element(By.ID, 'password')
        password.clear()
        password.send_keys(self.password)

        sleep(sleepsecs)
        self.driver.find_element(By.CLASS_NAME, "login__form_action_container")
        self.driver.find_element(By.TAG_NAME, "button").click()
        
        # 계정 정보 확인 팝업 페이지가 발생하면 '건너뛰기' 선택
        try:
            self.driver.find_element(By.CLASS_NAME, "secondary-action-new").click()
        except Exception as e:
            pass 



from selenium.webdriver.common.keys import Keys

"""검색조건 설정"""
class JobSearchAPI(object):
    keywords_writing_secs = 3

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
    def go_to_job(self):
        self.driver.get("https://www.linkedin.com/jobs/?")
    
    ############################## 구성요소 ##############################
    @property 
    def search_box(self): 
        return self.driver.find_element(By.ID, "global-nav-search")
    @property 
    def keyword_box(self): 
        return self.search_box.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword-id')]")
    @property 
    def location_box(self):
        div = self.search_box.find_element(By.XPATH, "//div[contains(@class, 'jobs-search-box__input')]")
        return div.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-location-id-')]")
    @property 
    def submit_button(self):
        return self.search_box.find_element(By.XPATH, "//button[contains(@class, 'jobs-search-box__submit-button')]")
    @property 
    def filter_bar(self):
        return self.driver.find_element(By.ID, 'search-reusables__filters-bar')
    @property 
    def date_filter(self):
        # return self.filter_bar.find_element(By.XPATH, "//button[contains(@aria-label, 'Date Posted filter')]")
        return self.filter_bar.find_element(By.ID, "hoverable-outlet-date-posted-filter-value")




    def set_inputs(self, keyword='Data Analytics', location='서울'):
        # ActionChains(self.driver)\
        #     .click_and_hold(self.keyword_box)\
        #     .send_keys(keyword)\
        #     .perform()
            
        # ActionChains(self.driver)\
        #     .click_and_hold(self.location_box)\
        #     .send_keys(location)\
        #     .perform()

        # """검색어 설정"""
        elem = self.keyword_box
        elem.clear()
        elem.send_keys(keyword)
        
        sleep(0.5)

        # """지역 설정"""
        elem = self.location_box
        elem.clear()
        elem.send_keys(location)

        sleep(0.5)

        ActionChains(self.driver)\
            .key_down(Keys.RETURN)\
            .perform()

    """
    duration=0 : past24hours
    duration=1 : past_week
    duration=2 : past_month
    duration=3 : anytime
    """
    def choose_date_posted(self, duration=0, error_cnt=0):

        date_filter = filterbar_section.find_element(By.XPATH, "//button[contains(@aria-label, 'Date Posted filter')]")
        
        # 드롭-다운 선택지 불러오기.
        sln.clicker(webelem=date_filter.find_element(By.TAG_NAME, 'li-icon'))
        facets = filterbar_section.find_element(By.ID, "date-posted-facet-values")
        values = facets.find_elements(By.TAG_NAME, 'li')
        # 기간 선택.
        sln.clicker(webelem=values[duration].find_element(By.TAG_NAME, 'label'), secs=1)
        # 필터 적용.
        sln.clicker(webelem=facets.find_element(By.XPATH, "//button[contains(@data-control-name, 'filter_pill_apply')]"), secs=3)

    def choose_sort_by(self, sort='date'):
        sleep(1)
        try:
            sort_section = self.driver.find_element(By.ID, 'sort-by-select')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
            if hasattr(self, 'sort_value'): delattr(self, 'sort_value')
        else:
            sort_button = sort_section.find_element(By.ID, "sort-by-select-trigger")
            sort_option = sort_section.find_element(By.ID, 'sort-by-select-options')
            cur_sort_value = sort_button.find_element(By.TAG_NAME, 'p').text
            if sort not in cur_sort_value:
                # 옵션 선택 팝업 클릭.
                sln.clicker(webelem=sort_button.find_element(By.TAG_NAME, 'p'))
                # 최종 옵션 선택 및 적용.
                class_pat = f"jobs-search-dropdown__option-button--{sort}"
                xpath = f"//button[contains(@class, '{class_pat}')]"
                sln.clicker(webelem=sort_option.find_element(By.XPATH, xpath), secs=2)
            self.sort_value = sort
        finally:
            return self










from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains



class ProfileDriver(object):

    url = 'https://www.linkedin.com/in/jonghyuk-lee/'

    def __init__(self, driver):
        self.driver = driver
        super().__init__()

    def scrolldown_upto_bottom(self):
        before_len = 1
        after_len = 2
        while after_len > before_len:
            print(f"{'-'*60}\n before_len : {before_len}\n after_len : {after_len}")
            cards = self.driver.find_elements_by_class_name('pv-profile-section')
            before_len = len(cards)
            for card in cards:
                ActionChains(self.driver).move_to_element(card).perform()
                try: h2 = card.find_element_by_class_name('pv-profile-section__card-heading')
                except Exception as e: pass
                else: print(f"h2 : {h2.text}")
            cards = self.driver.find_elements_by_class_name('pv-profile-section')
            after_len = len(cards)
        print(f"{'*'*60}\n before_len : {before_len}\n after_len : {after_len}")

    def click_editskill(self):
        x_edit_status = "//a[contains(@class, 'pv-profile-section__edit-action') and contains(@href, '/detail/skills/') and contains(@class, 'active')]"
        x_edit_btn = "//a[contains(@class, 'pv-profile-section__edit-action') and contains(@href, '/detail/skills/')]"
        edit_status = self.driver.find_elements_by_xpath(x_edit_status)
        if len(edit_status) is 0:
            try:
                edit_btn = self.driver.find_element_by_xpath(x_edit_btn)
            except Exception as e:
                print(f"{'#'*60}\n Exception : {e}")
                return False
            else:
                edit_btn.click()
                return True
        elif len(edit_status) is 1:
            print(f"Skills editting pop-up is active.")
        else:
            print(f"WTF")

    def collect_skills(self):
        items = self.driver.find_elements_by_class_name('pv-skills__category-list-item')
        return [item.text for item in items]



"""로봇이 아님을 증명하는 핸들러"""
class LinkedInDefender:


    def __init__(self):
        p_login_url = re.compile('https://www\.linkedin\.com/login/')
        p_robot_url = re.compile('https://www\.linkedin\.com/checkpoint/')
        print(f"{'='*60}\n LinkedInDefender.__init__() Starts.")
        super().__init__()
        print(f"{'='*60}\n LinkedInDefender.__init__() Ends.")

    def if_LinkedIn_is_pranking(self):
        if re.search(pattern=self.base_url, string=self.driver.current_url) is None:
            ############################################################ CASE.1
            if self.p_login_url.search(string=self.driver.current_url) is not None:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 링크드인이 장난질 치고 있는데, 강제 로그아웃시켰으므로 재로그인.")
                self.driver.find_element(By.ID, 'username').clear()
                self.driver.find_element(By.ID, 'username').send_keys(self.userid)
                self.driver.find_element(By.ID, 'password').clear()
                self.driver.find_element(By.ID, 'password').send_keys(self.pw)
                self.driver.find_element(By.CLASS_NAME, "login__form_action_container").find_element(By.TAG_NAME, "button").click()
            else:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 링크드인이 장난질 치고 있으므로, 검색 페이지로 회귀 후 5초간 기다리기.")
                self.driver.back()
                sleep(5)
            ############################################################ CASE.2
            if self.p_robot_url.search(string=self.driver.current_url) is not None:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n '로봇이 아닙니다' 검증페이지로 이동할 경우, 프로그렘 정지.")
            return True
        else:
            return False

