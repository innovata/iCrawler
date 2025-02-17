# -*- coding: utf-8 -*-
# CLI 를 이용한 사용법 


import os 
import sys 
import platform 



# 영상 다운로드
# url = "https://www.instagram.com/p/DEdEkCAonkF/?utm_source=ig_web_copy_link"
# url = "https://www.instagram.com/reel/DEaGMQkCH3S/?utm_source=ig_web_copy_link"

# 이미지 다운로드
# url = "https://www.instagram.com/p/DE6557JzN2Q/?utm_source=ig_web_copy_link"



"""
CLI 사용법 

python app\youtube\youtube03.py 
    FFMPEG_BIN_LOCATION="F:\__PROGRAMS_FILES_x64__\ffmpeg-2025-02-13-git-19a2d26177-full_build\bin"
    YOUTUBE_VIDEO_DOWNLOAD_PATH="D:\GABRIELE_DRIVE"

    https://youtube.com/watch?v=5JCH_8qzaiM&si=Ctb2s6pAJnVdlAg-
    https://youtube.com/watch?v=hStZzX3jeqs&si=fuCGCoWt8mnvXr3m
"""




if __name__ == "__main__":
    
    args = sys.argv 
    # print(args)
    excute_file = args.pop(0)

    # 호출할 함수
    # func_name = args.pop(0)
    # print(args)


    # 옵션(전역변수) 셋업
    # ffmpeg 경로설정 
    for arg in args:
        key, value = arg.split("=")
        os.environ[key] = value 
    # print(os.environ)


    # 패키지로딩
    computer_name = platform.uname().node 
    # print(computer_name)
    if computer_name == 'LX3-JLE69-KOR':
        sys.path.append("D:\\pypjts\\iCrawler\\src")
    elif computer_name == 'DP58-JLE69-KOR':
        sys.path.append("F:\\pypjts\\iCrawler\\src")
    from ipycrawl.crawlers.youtube import _yt_dlp  


    # 호출할 함수
    func_name = input("Enter an API function name: ")


    # 호출할 함수
    func = getattr(_yt_dlp, func_name)
    print('Executed Function:', func)


    # 공통 로그인
    

    # 사용자 입력 
    url = input("Input YouTube Target URL: ")
    print('URL: ' + url)
    
    # 실행
    func(url)
