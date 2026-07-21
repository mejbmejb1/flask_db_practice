# flask에서 Blueprint를 가져온다
# HTML 렌더링을 위한 render_template을 가져온다
from flask import Blueprint, render_template, url_for, redirect, request
# pybo.models 경로에서 Question(테이블 이름)을 가져온다
from pybo.models import Question

from pybo.forms import QuestionForm, AnswerForm 
from datetime import datetime
from pybo import db

# 'question'이라는 이름의 블루프린트를 생성하고, 이 블루프린트의 모든 URL 시작점(/question)을 지정
bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list(): # URL '/question/list/'로 접근했을 때 실행될 라우트 함수를 정의
    # 데이터베이스의 Question 테이블에서 모든 질문 데이터를 가져온다
    # 작성일(create_date)의 역순(desc - 최신순)으로 정렬하여 question_list 변수에 담는다.
    question_list = Question.query.order_by(Question.create_date.desc())
    # 준비된 질문 목록(question_list) 데이터를 템플릿(HTML) 파일에 전달하며 화면을 그린다(렌더링)
    return render_template('question/question_list.html', question_list=question_list)

# /detail/question_id 번호 처리 라우트
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm() # 상세 조회 라우터 내부에 빈 답변 폼 생성
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

# 질문 등록 라우트 함수 추가
@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 등록할 내용을 Question table에 넣어서 등록한다
        target_question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        log_temp = target_question.__repr__()
        print(log_temp)
        db.session.add(target_question)
        db.session.commit()
        return redirect(url_for('question._list'))    
    return render_template('question/question_form.html', form=form)