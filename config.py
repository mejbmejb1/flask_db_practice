import os
'''
    config.py
        1. BASE_DIR = 현재 프로젝트의 루트 폴더 경로
        2. SQLALCHEMY_DATABASE_URI = 플라스크 ORM 라이브러리인 SQLAlchemy가 어떤 데이터베이스에 연결해야 하는지 결정하는 접속 경로 설정 변수
            - 프로젝트 폴더 위치(BASE_DIR)를 찾는다
            - pybo.db라는 이름으로 데이터베이스 파일을 만들거나 읽으라는 절대 경로
        3. SQLALCHEMY_TRACK_MODIFICATIONS = SQLAlchemy가 객체의 변경을 자동으로 추적하는 기능 설정
            - false 설정 배경: 메모리 사용량을 줄이고 불필요한 경고를 줄인다

'''

BASE_DIR = os.path.dirname(__file__)
#print(BASE_DIR)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

SQLALCHEMY_TRACK_MODIFICATIONS = False

# 비밀키 추가: CSRF 토큰 생성
SECRET_KEY = "dev"