from flask import Flask, render_template, redirect, url_for, flash
from forms import RegistrationForm

app = Flask(__name__)
# Flask-WTF의 CSRF 보안 기능을 작동시키려면 SECRET_KEY가 반드시 필요합니다.
app.config['SECRET_KEY'] = 'your-very-secret-key'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # validate_on_submit()은 요청이 'POST'이고,
    # 위의 forms.py에 지정한 모든 validators를 통과했을 때만 True를 반환합니다.
    if form.validate_on_submit():
        # 검증 완료된 데이터는 form.필드명.data로 접근합니다.
        user_email = form.email.data
        flash(f'{form.username.data}님, 회원가입을 축하합니다!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/')
def home():
    return "홈페이지"

if __name__ == '__main__':
    app.run(debug=True)