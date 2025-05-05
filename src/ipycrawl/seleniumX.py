# -*- coding: utf-8 -*-
"""
Selenium-eXtension 
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import pprint 
pp = pprint.PrettyPrinter(indent=2)


from ipylib.idebug import *


import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_driver():
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    print("\nOptions -->")
    pp.pprint(options.__dict__)

    driver = webdriver.Edge(options=options)
    print("\nDriver -->")
    pp.pprint(driver.__dict__)
    return driver


"""엔터키 누르기"""
def press_enter(driver):
    ActionChains(driver)\
        .key_down(Keys.RETURN)\
        .perform()
    

"""입력박스에 값 쓰기"""
def fill_inputBox(driver, element, value, wait=1):
    ActionChains(driver)\
        .move_to_element(element)\
        .pause(wait)\
        .click_and_hold()\
        .pause(wait)\
        .send_keys(value)\
        .perform()
    
