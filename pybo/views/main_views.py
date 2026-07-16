from flask import Blueprint, redirect, url_for

# 애플리케이션의 라우트(URL)와 기능을 모듈화하여 관리하는 디자인 패턴
bp = Blueprint('main', __name__, url_prefix='/')

'''
#route('')
/ = root

'''

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo~!~!~!~!~'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))