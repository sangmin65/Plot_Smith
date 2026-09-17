from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 💡 MySQL 접속 정보 설정
# 형식: mysql+pymysql://유저이름:비밀번호@호스트주소:포트번호/데이터베이스이름
# 주의: '본인비밀번호' 자리에 실제 MySQL root 비밀번호를 입력하세요! (예: root:1234@localhost...)
DB_URL = "mysql+pymysql://root:181844mM%40@localhost:3306/plot_smith"

# DB 엔진 생성 (echo=True로 설정하면 터미널에서 SQL 실행 로그를 볼 수 있습니다)
engine = create_engine(DB_URL, echo=True)

# DB 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 베이스 클래스
Base = declarative_base()

# 💡 API가 호출될 때마다 DB 세션을 열고 닫아주는 의존성(Dependency) 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()