# 이 파이썬 파일을 실행하면 'admin' 이름

from pybo import create_app, db
from pybo.models import User
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Flask 애플리케이션 객체 생성
app = create_app()

# 2. 애플리케이션 컨텍스트 내부에서 데이터베이스 작업 수행
with app.app_context():
    print("테스트 데이터 생성 시작...")    

    user_admin = [
        User(
            id = 0,
            username = 'admin',
            password = generate_password_hash('asdf'),
            email = 'admin@admin.com'
        )
    ]
    
    # bulk_save_objects를 생성한 계정 db에 추가
    db.session.bulk_save_objects(user_admin)
    
    # 최종 커밋
    db.session.commit()

    print("계정 생성이 완료됐습니다")
    pass_value = input("종료하려면 enter를 누르세요")
