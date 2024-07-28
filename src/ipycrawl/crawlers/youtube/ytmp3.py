# -*- coding: utf-8 -*-
# https://en.ytmp3.nu/ --> 안된다 
# https://ytmp3.cc/ 웹사이트를 이용해서 mp3를 다운로드하는 기능을 제공한디.






from PyQt5.QtCore import QObject
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def get_driver():
    return webdriver.Chrome()


class YTMP3Client(QObject):

    def __init__(self):
        super().__init__()
        self.driver = get_driver()
        self.driver.get("https://ytmp3.cc/")

    def download(self, url):
        input_box = self.driver.find_element(By.ID, "video")
        input_box.send_keys(url)
        input_box.send_keys(Keys.RETURN)

        try:
            download_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "download"))
            )
        finally:
            download_button = download_button.find_element(By.TAG_NAME, 'a')
            download_button.click()

            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'Convert next'))
                )
            finally:
                next_button.click()
                self.close_redirect_tabs()

    # 다운로드시 자동으로 리다이렉되는 탭들을 모두 닫는다 
    def close_redirect_tabs(self):
        handles = self.driver.window_handles
        if len(handles) == 1:
            pass 
        else:
            handles.pop(0)
            for handle in handles:
                self.driver.switch_to.window(handle)
                self.driver.close()







            













