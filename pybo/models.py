'''
models.py
    - 관련 DB 모델을 생성하고 관리하는 곳
    - ondelete='CASCADE': 질문이 삭제되었을 때 그에 달린 답변들도 함께 삭제되도록 한 설정은 데이터베이스의 무결성(데이터의 일관성)을 지키는 데 필수

'''
from pybo import db
from sqlalchemy import Table

max_string = 200

# 중간 테이블 정의
question_voter = Table(
    'question_voter', # 데이터베이스에서 쓸 이름
    db.metadata, # 데이터베이스에서 한꺼번에 관리하기 위해 db 설계도에 등록
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = Table(
    'answer_voter',
    db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(max_string), nullable=False) # 200자까지 문자열 제한이 있으며 null을 허용하지 않겠다.
    content = db.Column(db.Text(), nullable=False) 
    create_date = db.Column(db.DateTime(), nullable=False) # DateTime을 받아오며 null을 허용하지 않겠다
    # 업로드된 이미지 경로 추가
    image_path = db.Column(db.String(max_string), nullable=True)
    # 글쓴이 외래키 및 관계 설정 추가
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    # 추천인 (多대多)
    voter = db.relationship('User', secondary=question_voter,
                            backref=db.backref('question_voter_set', lazy='dynamic'))

    # 쉘이나 로그에서 객체를 보기 쉽게 출력해주는 메서드
    def __repr__(self):
        if self.subject: # subject에 글자가 들어있다면(슬라이싱중 index 에러방어)
            subject_preview = self.subject[:50]
        else: # subject가 비어있거나 None이라면
            subject_preview = "No Title"
        return f'<Question {self.user_id}: {subject_preview}>'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    voter = db.relationship('User', secondary=answer_voter,
                            backref=db.backref('answer_voter_set', lazy='dynamic'))

    def __repr__(self):
        return f'<Answer to Question {self.question_id}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False) # unique = True 중복 막겠다
    password = db.Column(db.String(max_string), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    # 질문 테이블 및 답변 테이블과의 다대일(N:1) 관계 외래키 매핑
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))