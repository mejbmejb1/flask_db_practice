from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pybo.filter import format_datetime

import markdown 
from markupsafe import Markup

import config

# DB 생성자
db = SQLAlchemy()
# 관리자
migrate = Migrate()


def create_app(): #applictaion factory 함수
    app = Flask(__name__) # pybo 
    # config.py 파일에 작성한 항목을 읽기 위해 추가
    app.config.from_object(config)

    # ORM (Object-Relational Mapping) 초기화
    from .import models
    db.init_app(app) # db 초기화
    migrate.init_app(app, db) # app과 db를 연결한다
    
    # blueprint 등록
    from .views import main_views, question_views, answer_views, auth_views, comment_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)

    def format_markdown(text):
        if not text:
            return ""
        
        # markdown.markdown()의 결과(문자열)를 MarkupSafe의 Markup 객체로 감싸줍니다.
        # 이렇게 감싸주어야 템플릿(HTML)에서 꺾쇠 태그가 무력화되지 않고 화면에 잘 나옵니다.
        # nl2br         : 줄바꿈을 <br>로 변환
        # fenced_code   : 코드 블록 지원, <pre><code>로 변환
        # sane_lists    : 번호 목록 작성 시 오동작 방지
        # tables        : 표(Table) 구문 지원
        # toc           : 제목(Header) ID 생성 및 목차 지원 
        html_content = markdown.markdown(text, extensions=['nl2br', 'fenced_code', 'sane_lists', 'tables', 'toc'])

        # 테이블 테그를 생성하여 테이블 적용 코드
        html_content = html_content.replace(
            '<table>',
            '<table class="table table-bordered table-hover">'
        )
        
        return Markup(html_content)

    # jinja_env 필터에 등록
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['markdown'] = format_markdown

    return app