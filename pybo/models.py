from pybo import db

'''
models.py
    - 관련 DB 모델을 생성하고 관리하는 곳
    - ondelete='CASCADE': 질문이 삭제되었을 때 그에 달린 답변들도 함께 삭제되도록 한 설정은 데이터베이스의 무결성(데이터의 일관성)을 지키는 데 필수

'''

max_string = 200

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(max_string), nullable=False) # 200자까지 문자열 제한이 있으며 null을 허용하지 않겠다.
    content = db.Column(db.Text(), nullable=False) 
    create_date = db.Column(db.DateTime(), nullable=False) # DateTime을 받아오며 null을 허용하지 않겠다

    # 쉘이나 로그에서 객체를 보기 쉽게 출력해주는 메서드
    def __repr__(self):
        if self.subject: # subject에 글자가 들어있다면(슬라이싱중 index 에러방어)
            subject_preview = self.subject[:10]
        else: # subject가 비어있거나 None이라면
            subject_preview = "No Title"
        return f'<Question {self.id}: {subject_preview}>'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f'<Answer to Question {self.question_id}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(max_string), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)