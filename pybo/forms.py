'''
forms.py
    각 필드에 적용하는 검증 규칙을 정한다

'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    # 1. 필수 입력 + 길이 제한
    username = StringField('사용자 이름', validators=[
        DataRequired(message="이름은 필수 입력 항목입니다."),
        Length(min=2, max=20, message="이름은 2자 이상 20자 이하로 입력해주세요.")
    ])

    # 2. 필수 입력 + 이메일 형식
    email = StringField('이메일', validators=[
        DataRequired(message="이메일은 필수 입력 항목입니다."),
        Email(message="올바른 이메일 형식이 아닙니다.")
    ])

    # 3. 필수 입력 + 비밀번호 확인 일치 여부
    password = PasswordField('비밀번호', validators=[
        DataRequired(message="비밀번호는 필수 입력 항목입니다.")
    ])
    confirm_password = PasswordField('비밀번호 확인', validators=[
        DataRequired(message="비밀번호 확인을 입력해주세요."),
        EqualTo('password', message="비밀번호가 일치하지 않습니다.")
    ])

    submit = SubmitField('가입하기')

    # 4. 커스텀 검증기 (Custom Validator)
    # validate_필드명 형태로 메서드를 만들면 해당 필드를 검증할 때 자동으로 실행됩니다.
    def validate_username(self, username):
        banned_names = ['admin', 'root', 'administrator']
        if username.data.lower() in banned_names:
            raise ValidationError('사용할 수 없는 이름입니다.')
        
# 제목(subject), 내용(content) 필드에 필수 입력임을 알리는 class  
class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])
    image = FileField('이미지 업로드', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '이미지 파일만 업로드 가능합니다.')])

# 답변 검증용 폼 클래스 추가
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])


class UserCreateForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(),
        EqualTo('password2', message='비밀번호가 일치하지 않습니다.')
    ])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

# 로그인 폼 클래스 추가
class UserLoginForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])