from datetime import datetime
from flask import Blueprint, url_for, request, redirect, render_template
from pybo import db
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>/', methods=('POST',))
def create(question_id):
    # Question 테이블에서 id 값 보고 조회하는데 없으면 404에러 보냄
    question = Question.query.get_or_404(question_id)
    # 'content' 추출
    content = request.form['content']
    answer = Answer(content=content, create_date=datetime.now())
    question.answer_set.append(answer)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))