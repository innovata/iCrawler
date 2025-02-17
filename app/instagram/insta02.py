# -*- coding: utf-8 -*-



import os 
import sys 
import platform 


sys.path.append("D:\\pypjts\\iCrawler\\src")
from ipycrawl.crawlers.instagram import _instagrapi 





# 영상 다운로드
# url = "https://www.instagram.com/p/DEdEkCAonkF/?utm_source=ig_web_copy_link"
# url = "https://www.instagram.com/reel/DEaGMQkCH3S/?utm_source=ig_web_copy_link"

# 이미지 다운로드
# url = "https://www.instagram.com/p/DE6557JzN2Q/?utm_source=ig_web_copy_link"

# 사용자 입력
# url = input("Input your Instagram URL: ")

# _instagrapi.login('ghost')
# _instagrapi.download_video(url)
# _instagrapi.download_image(url)



# https://www.instagram.com/reel/DC1JCBsCXwS/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==

if __name__ == "__main__":
    
    print(sys.argv)

    # 호출할 함수
    func_name = sys.argv[1]
    func = getattr(_instagrapi, func_name)
    print('Executed Function:', func)


    # 공통 로그인
    _instagrapi.login('gabriele')

    # 사용자 입력
    url = input("Input your Instagram URL: ")
    print('URL: ' + url)
    # 실행
    func(url)
