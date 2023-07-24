# iCrawler

Web Crawlling, Scrapying 또는 OpenAPI 를 사용하여 데이타를 수집하는 Innovata-Crawler

기존 개별 프로젝트들에서 구현했던 스크랩 기능들을 한군데 모아서 이 패키지를 API화 하는 것을 목표로 한다. (계속 추가 중)



# OpenAPI Credentials 사용법

## 1. Saramin OpenAPI 


Saramin 채용정보 API 웹페이지에서 회원가입을 하고 로그인 한 후, 절차에 따라 액세스 키를 발급받는다.

    https://oapi.saramin.co.kr/

발급받은 액세스 키는 다음과 같은 형식으로 파일명을 'credential.json' 으로 생성하고, 임의의 경로에 저장한 뒤 '절대경로'를 복사해둔다.

    {
        "사람인": {
            "ACCESS_KEY": "YOUR_ACCESS_KEY",
            "USER_ID": "YOUR_ID",
            "USER_PASSWORD": "YOUR_PASSWORD"
        },
        "LinkedIn": {
            "USER_ID": "YOUR_ID",
            "USER_PASSWORD": "YOUR_PASSWORD"
        },
        ...
    }

Jupyter 파일을 열고 커널을 선택한 후, 첫번째 셀에서 ipycrawl 패키지를 임포트 하기 전에 조금 전에 복사해 둔 '절대경로'를 아래와 같이 설정한다.

    import os

    os.environ['CREDENTIAL_PATH']=YOUR_CREDENTIAL_JSON_FILE_PATH



## 2. 공공데이터포털 (DATA.GO.KR) OpenAPI

## 3. 한국은행 (EOS) OpenAPI

## 4. 통계청 (SGIS) OpenAPI