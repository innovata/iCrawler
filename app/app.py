# -*- coding: utf-8 -*-



import os 
import sys 











if __name__ == "__main__":
    
    print(sys.argv)

    # 호출할 함수
    func_name = sys.argv[1]
    func = getattr(_instagrapi, func_name)
    print('Executed Function:', func)

    # 사용자 입력
    url = input("Input your Instagram URL: ")
    print('URL: ' + url)

    # 공통 로그인
    _instagrapi.login('ghost')

    # 실행
    func(url)