from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database import get_db

app = FastAPI(title="Plot_Smith v2.0 API", description="서사 무결성 검증 엔진")

@app.get("/")
def read_root():
    return {"message": "Plot_Smith 백엔드 서버가 정상적으로 실행 중입니다. 🚀"}

# 💡 DB 연결 테스트용 API 엔드포인트
@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # DB에 접속해서 테이블 목록을 가져오는 간단한 SQL 쿼리 실행
        result = db.execute(text("SHOW TABLES;")).fetchall()
        tables = [row[0] for row in result]
        
        return {
            "status": "success", 
            "message": "🎉 MySQL 데이터베이스 연결 성공!", 
            "tables": tables
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"DB 연결 실패: {str(e)}"
        }
    

from pydantic import BaseModel

# 💡 클라이언트(프론트)에서 보낼 원고 데이터 구조 정의
class ChapterInput(BaseModel):
    project_id: int
    chapter_number: int
    content: str

# 💡 핵심 QA 검증 엔진 API
@app.post("/api/qa/analyze")
def analyze_chapter(req: ChapterInput, db: Session = Depends(get_db)):
    # 1. DB에서 해당 작품의 '사망한(DEAD)' 캐릭터 목록 조회
    query = text("SELECT char_id, name FROM Characters WHERE project_id = :pid AND status = 'DEAD'")
    dead_chars = db.execute(query, {"pid": req.project_id}).fetchall()
    
    errors = []
    
    # 2. 작가가 쓴 텍스트(content) 안에 사망한 캐릭터 이름이 등장하는지 검사
    for char in dead_chars:
        char_id, name = char[0], char[1]
        
        if name in req.content: # 원고에 죽은 캐릭터 이름이 감지되면!
            error_msg = f"⚠️ [생사 오류] {req.chapter_number}화: 사망 처리된 캐릭터 '{name}'(이)가 원고에 등장했습니다."
            errors.append(error_msg)
            
            # (선택) DB의 Validation_Logs 테이블에 에러 기록 저장
            log_query = text("""
                INSERT INTO Validation_Logs (project_id, chapter_id, error_type, message)
                VALUES (:pid, 1, 'DEATH_VIOLATION', :msg) 
            """)
            db.execute(log_query, {"pid": req.project_id, "msg": error_msg})
            db.commit()
            
    # 3. 결과 반환
    if errors:
        return {"status": "conflict_detected", "errors": errors}
    
    return {"status": "clean", "message": "✨ 무결성 검증 통과! 설정 충돌이 없습니다."}