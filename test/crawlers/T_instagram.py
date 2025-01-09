# -*- coding: utf-8 -*-

import unittest
import sys 
import pprint 
pp = pprint.PrettyPrinter(indent=2)
import os 
import platform 


COMPUTER_NAME = platform.uname().node
print('COMPUTER_NAME: ', COMPUTER_NAME)

if COMPUTER_NAME == "RYZEN9-X570-AORUS-ELITE":
    os.environ['INSTAGRAM_CREDENTIAL_PATH'] = "J:\\내 드라이브\\__CREDENTIALS__\\INSTAGRAM\\credentials.json"
    os.environ['INSTAGRAM_DOWNLOAD_PATH'] = "D:\\LatinDanceData\\Instagram"
    
elif COMPUTER_NAME == "":
    os.environ['INSTAGRAM_CREDENTIAL_PATH'] = "H:\\My Drive\\__CREDENTIALS__\\INSTAGRAM\\credentials.json"
    os.environ['INSTAGRAM_DOWNLOAD_PATH']




sys.path.append("D:\\pypjts\\iCrawler\\src")
from ipycrawl.crawlers.instagram import _instagrapi
from ipycrawl.crawlers.instagram.models import InstaMedia




# @unittest.skip("module")
class ipycrawl_crawlers_instagram_models(unittest.TestCase):

    def setUp(self):
        print('\n\n')

    def test01(self):
        m = InstaMedia("https://www.instagram.com/reel/DEaGMQkCH3S/?utm_source=ig_web_copy_link")
        pp.pprint(m.__dict__)











if __name__ == "__main__":
    unittest.main(
        module='__main__',
        argv=None,
        testRunner=None,
        testLoader=unittest.defaultTestLoader,
        verbosity=2,
        failfast=None,
        buffer=None,
        warnings=None
    )