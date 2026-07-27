from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pybo.filter import format_datetime

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

    # jinja_env 필터에 등록
    app.jinja_env.filters['datetime'] = format_datetime

    return app