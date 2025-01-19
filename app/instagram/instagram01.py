# -*- coding: utf-8 -*-



import os 
import sys 
import platform 


COMPUTER_NAME = platform.uname().node
print('COMPUTER_NAME: ', COMPUTER_NAME)

if COMPUTER_NAME == "RYZEN9-X570-AORUS-ELITE":
    os.environ['INSTAGRAM_CREDENTIAL_PATH'] = "J:\\내 드라이브\\__CREDENTIALS__\\INSTAGRAM\\credentials.json"
    os.environ['INSTAGRAM_DOWNLOAD_PATH'] = "D:\\__GABRIELE_DRIVE__\\LatinDanceData\\Instagram"
    
elif COMPUTER_NAME == "":
    os.environ['INSTAGRAM_CREDENTIAL_PATH'] = "H:\\My Drive\\__CREDENTIALS__\\INSTAGRAM\\credentials.json"
    os.environ['INSTAGRAM_DOWNLOAD_PATH']


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


    # 컬렉션
    # collections = _instagrapi.get_collections()
    # print('\nCollections--> Count: %s' % len(collections))
    # for c in collections: print(c)

    # medias = _instagrapi.get_medias_of_collection(collections[0])
    # print('\nMedias--> Count: %s' % len(medias))
    # for m in medias[:5]: print('\n\n', m)


    # _instagrapi.download_collection_medias('All posts')