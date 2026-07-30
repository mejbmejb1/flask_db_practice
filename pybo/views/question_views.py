# flask에서 Blueprint를 가져온다
# HTML 렌더링을 위한 render_template을 가져온다
from flask import Blueprint, render_template, url_for, redirect, request, g, flash, current_app
# pybo.models 경로에서 Question(테이블 이름)을 가져온다
from pybo.models import Question, Answer, User, question_voter

from pybo.forms import QuestionForm, AnswerForm 
from datetime import datetime
from pybo import db
from pybo.views.auth_views import login_required
from sqlalchemy import func, distinct # func 파이썬에세 SQL 함수를 사용 가능하게 도와준다
from werkzeug.utils import secure_filename # DB 경로 저장 처리
import os
import uuid

# 'question'이라는 이름의 블루프린트를 생성하고, 이 블루프린트의 모든 URL 시작점(/question)을 지정
bp = Blueprint('question', __name__, url_prefix='/question')

# 공통으로 사용하는 내용을 변수화
per_page_num = 10
default_page = 1

@bp.route('/list/')
def _list(): # URL '/question/list/'로 접근했을 때 실행될 라우트 함수를 정의
    # 현재 페이지 번호 가져오기 (기본값은 1)
    page = request.args.get('page', type=int, default=default_page)
    kw = request.args.get('kw', type=str, default='')   # 검색어
    so = request.args.get('so', type=str, default='recent')  # 정렬 기준

    # 기본 쿼리
    question_list = Question.query

    # 2. 검색 (kw) 조건 처리
    if kw:
        search = '%%{}%%'.format(kw)
        # 검색한 글에서 답변있는지 확인한다
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username).join(User, Answer.user_id == User.id).subquery()

        question_list = (question_list 
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    Question.user.has(User.username.ilike(search)) |
                    sub_query.c.username.ilike(search)))

    # 3. 정렬 (so) 및 그룹화 처리
    if so == 'recommend':
        # 매핑 테이블(question_voter)을 직접 outerjoin하고, 그 안의 user_id 개수를 distinct하게 집계합니다.
        question_list = (question_list
            .outerjoin(question_voter, Question.id == question_voter.c.question_id) 
            .group_by(Question.id)
            .order_by(func.count(distinct(question_voter.c.user_id)).desc(), Question.create_date.desc()))

    elif so == 'popular':
        # 인기순 정렬 (답변수 기준)
        question_list = (question_list
            .outerjoin(Answer, Answer.question_id == Question.id)
            .group_by(Question.id)
            .order_by(func.count(distinct(Answer.id)).desc(), Question.create_date.desc()))

    else:  # recent (최신순)
        question_list = (question_list
        .group_by(Question.id)
        .order_by(Question.create_date.desc()))

    # 데이터베이스의 Question 테이블에서 모든 질문 데이터를 가져온다
    # 작성일(create_date)의 역순(desc - 최신순)으로 정렬하여 question_list 변수에 담는다. + 한 페이지당 개수를 조회하는 기능 추가(paginate)    
    question_list = question_list.paginate(page=page, per_page=per_page_num)
    # 준비된 질문 목록(question_list) 데이터를 템플릿(HTML) 파일에 전달하며 화면을 그린다(렌더링)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, so=so)

# /detail/question_id 번호 처리 라우트
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm() # 상세 조회 라우터 내부에 빈 답변 폼 생성
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

# 질문 등록 라우트 함수 추가
@bp.route('/create/', methods=('GET', 'POST'))
@login_required # 해당 메서드 만족해야 def create() 실행가능
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():

        # to apply image - check log
        border_for_log = 50
        print("=" * border_for_log)
        print("request.files :", request.files)
        print("image.data    :", form.image.data)
        print("filename      :", form.image.data.filename if form.image.data else None)
        print("root_path     :", current_app.root_path) # 현재 실행하고 있는 flask app에 접근하기 위한 객체(current_app)
        print("=" * border_for_log)

        # 폼에서 전송된 이미지 파일
        image_file = form.image.data
        image_path = None

        if image_file:
            # 저장 경로 : 오늘 날짜로 폴더 생성
            today = datetime.now().strftime('%Y%m%d')
            upload_folder = os.path.join(current_app.root_path, 'static/photo', today)
            os.makedirs(upload_folder, exist_ok=True)

            # 파일 저장
            # 사용자가 업로드한 파일명을 운영체제에서 안전하게 사용할 수 있는 형태로 변환하여, 
            # 경로 조작(Path Traversal) 등의 보안 위험을 줄여 주는 함수
            filename = secure_filename(image_file.filename)
            print("filename ====> " , filename)

            ext = os.path.splitext(image_file.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            
            file_path = os.path.join(upload_folder, filename)
            image_file.save(file_path)

            # DB에 저장할 경로 (static 기준 상대경로)
            image_path = f'photo/{today}/{filename}'            

        # 등록할 내용을 Question table에 넣어서 등록한다
        target_question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user= g.user, image_path=image_path)
        log_temp = target_question.__repr__()
        print(log_temp)
        db.session.add(target_question)
        db.session.commit()
        return redirect(url_for('question._list'))    
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>/', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question) # 폼 데이터를 question 객체에 동적 복사
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        # GET 요청일 경우 기존 데이터를 폼에 채워서 렌더링
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>/')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    question = Question.query.get_or_404(question_id)

    # 로그인한 사용자가 본인의 글을 추천하는 것을 막음.
    if g.user == question.user:
        flash('본인이 작성한 글은 추천할 수 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    # 중복 추천 방지 로직
    if g.user in question.voter:
        flash('이미 추천한 질문입니다')
        return redirect(url_for('question.detail', question_id=question_id))
    
    # 기존 추천 처리 로직
    question.voter.append(g.user)
    db.session.commit()
    
    return redirect(url_for('question.detail', question_id=question_id))