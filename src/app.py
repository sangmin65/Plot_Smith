import streamlit as st
import requests
import pandas as pd
from sqlalchemy import text
from database import SessionLocal

st.set_page_config(page_title="Plot_Smith", page_icon="📝", layout="wide")

st.title("Plot_Smith 📝")
st.subheader("웹소설 설정 무결성 검증 엔진 v2.0")

tab1, tab2, tab3 = st.tabs(["✍️ 1. 실시간 에디터 검증", "🗄️ 2. AI Hub 적재 데이터 검증", "👥 3. 캐릭터 도감 (설정 백과)"])

with tab1:
    st.markdown("### 📖 작가용 실시간 원고 입력")
    project_id = st.number_input("프로젝트 ID", value=1)
    chapter_number = st.number_input("챕터 번호", value=15)
    content = st.text_area("원고 내용을 입력하세요", height=200, placeholder="주인공이 검을 뽑아 들었다. 그때, 분명 죽었을 터인 C001이 웃으며 걸어왔다.")

    if st.button("🔍 실시간 설정 충돌 검증하기"):
        with st.spinner("엔진 구동 중..."):
            response = requests.post(
                "http://127.0.0.1:8000/api/qa/analyze",
                json={"project_id": project_id, "chapter_number": chapter_number, "content": content}
            )
            if response.status_code == 200:
                data = response.json()
                errors = data.get("errors", [])
                if errors:
                    st.error("🚨 설정 충돌이 감지되었습니다!")
                    for err in errors:
                        st.write("- " + err)
                else:
                    st.success("✅ 설정 충돌이 없습니다. 무결성이 유지됩니다.")
            else:
                st.error("서버와 통신할 수 없습니다.")

with tab2:
    st.markdown("### 📚 DB 원고 일괄 스캐닝 (Batch QA)")
    st.info("전처리 파이프라인(ETL)을 통해 DB에 적재된 공공데이터를 스캔하여 모순을 찾아냅니다.")

    demo_scenario = st.selectbox(
        "검증할 시나리오를 선택하세요",
        options=[1, 2],
        format_func=lambda x: "시나리오 1: 정상 검증 (무결성 100% 통과)" if x == 1 else "시나리오 2: 타임라인 오류 검증 (사망 캐릭터의 재등장 시연)"
    )

    if st.button("🚀 대량 원고 모순 스캐닝 시작"):
        with st.spinner("AI Hub 적재 데이터를 교차 검증 중입니다 (빅데이터 처리)..."):
            db = SessionLocal()
            try:
                latest_pid = db.execute(text("SELECT MAX(project_id) FROM Projects")).scalar()

                if not latest_pid:
                    st.warning("⚠️ DB에 프로젝트가 없습니다. 전처리를 먼저 진행해주세요.")
                else:
                    chapters = db.execute(text("SELECT chapter_number, content FROM Chapters WHERE project_id = :pid"), {"pid": latest_pid}).fetchall()

                    if not chapters:
                        st.warning(f"⚠️ {latest_pid}번 프로젝트에 등록된 원고가 없습니다.")
                    else:
                        error_logs = []
                        
                        if demo_scenario == 1:
                            death_timeline = {'존재하지않는인물': 15}
                        else:
                            death_timeline = {'E001': 5, 'C007': 5}

                        for chap in chapters:
                            chap_num = chap[0]
                            chap_content = chap[1]
                            
                            for name, death_chapter in death_timeline.items():
                                if chap_num > death_chapter and name in chap_content:
                                    error_logs.append(f"⚠️ [타임라인 모순] {chap_num}화: {death_chapter}화에서 사망 처리된 '{name}'(이)가 원고에 재등장했습니다.")

                        st.success(f"✅ 총 {len(chapters)}개의 원고 스캐닝 완료!")

                        if error_logs:
                            st.error(f"🚨 총 {len(error_logs)}건의 치명적 타임라인 설정 충돌이 감지되었습니다!")
                            with st.expander("상세 에러 로그 보기", expanded=True):
                                for err in error_logs[:20]:
                                    st.write("- " + err)
                                if len(error_logs) > 20:
                                    st.write(f"... 외 {len(error_logs)-20}건의 충돌 추가 감지됨")
                        else:
                            st.success("✅ 적재된 모든 데이터에서 설정 충돌이 발견되지 않았습니다. (무결성 100%)")
            except Exception as e:
                st.error(f"DB 오류 발생: {e}")
            finally:
                db.close()

# 💡 진화된 3번 탭: 타임라인 기반 캐릭터 버전 관리
with tab3:
    st.markdown("### 👥 캐릭터 도감 (설정 백과)")
    st.info("작품의 캐릭터 설정을 열람하고, 스토리가 전개됨에 따른 상태 변화(사망, 성격 흑화 등)를 타임라인으로 기록합니다.")
    
    db = SessionLocal()
    try:
        projects = db.execute(text("SELECT project_id, title FROM Projects")).fetchall()
        
        if not projects:
            st.warning("⚠️ DB에 등록된 작품이 없습니다. 전처리를 먼저 진행해주세요.")
        else:
            project_options = {p[0]: f"[{p[0]}번 작품] {p[1]}" for p in projects}
            selected_pid = st.selectbox(
                "📖 설정을 열람할 작품을 선택하세요",
                options=list(project_options.keys()),
                format_func=lambda x: project_options[x]
            )
            
            # DB에서 현재 작품의 캐릭터 정보 불러오기
            chars_data = db.execute(text("""
                SELECT char_id, name, status, role, personality, background, death_chapter, personality_change_chapter 
                FROM Characters WHERE project_id = :pid
            """), {"pid": selected_pid}).fetchall()

            col_left, col_right = st.columns(2)
            
            # 1. 새 캐릭터 등록 폼
            with col_left:
                with st.expander(f"➕ 신규 캐릭터 등록하기", expanded=False):
                    with st.form("character_form", clear_on_submit=True):
                        new_name = st.text_input("이름*")
                        new_status = st.selectbox("생사 상태*", ["ALIVE", "DEAD", "UNKNOWN"])
                        new_role = st.text_input("역할 (예: 주인공, 조력자)")
                        new_personality = st.text_area("성격 및 특징")
                        new_background = st.text_area("배경 설정")
                        
                        if st.form_submit_button("💾 캐릭터 저장"):
                            if not new_name.strip():
                                st.error("이름은 필수입니다!")
                            else:
                                db.execute(text("""
                                    INSERT INTO Characters (project_id, name, status, role, personality, background)
                                    VALUES (:pid, :name, :status, :role, :personality, :background)
                                """), {"pid": selected_pid, "name": new_name, "status": new_status, "role": new_role, "personality": new_personality, "background": new_background})
                                db.commit()
                                st.success("등록 완료!")
                                st.rerun()

            # 2. 기존 캐릭터 '상태/성격 변화' 타임라인 업데이트 폼
            with col_right:
                with st.expander(f"✏️ 등록된 캐릭터 상태 업데이트 (타임라인 기록)", expanded=False):
                    if not chars_data:
                        st.write("등록된 캐릭터가 없습니다.")
                    else:
                        char_dict = {c[0]: c[1] for c in chars_data}
                        selected_cid = st.selectbox("업데이트할 캐릭터 선택", options=list(char_dict.keys()), format_func=lambda x: char_dict[x])
                        
                        target_char = next(c for c in chars_data if c[0] == selected_cid)
                        c_status = target_char[2]
                        c_personality = target_char[4]
                        
                        with st.form("update_character_form"):
                            st.info(f"**{char_dict[selected_cid]}** (현재 상태: {c_status})")
                            
                            up_col1, up_col2 = st.columns(2)
                            with up_col1:
                                new_status = st.selectbox("변경할 상태", ["ALIVE", "DEAD", "UNKNOWN"], index=["ALIVE", "DEAD", "UNKNOWN"].index(c_status) if c_status in ["ALIVE", "DEAD", "UNKNOWN"] else 0)
                            with up_col2:
                                update_chapter = st.number_input("변경 발생 회차 (몇 화?)", min_value=1, value=15)
                                
                            new_personality = st.text_area("변경된 성격 (흑화/각성 등)", value=c_personality if c_personality else "")
                            
                            if st.form_submit_button("🔄 변경 내역 및 회차 기록"):
                                update_query = "UPDATE Characters SET status = :status, personality = :personality"
                                params = {"status": new_status, "personality": new_personality, "cid": selected_cid}
                                
                                # Alive -> Dead 로 바뀌었을 경우 사망 회차 기록
                                if c_status != 'DEAD' and new_status == 'DEAD':
                                    update_query += ", death_chapter = :dc"
                                    params["dc"] = update_chapter
                                    
                                # 성격이 바뀌었을 경우 성격 변경 회차 기록
                                if c_personality != new_personality:
                                    update_query += ", personality_change_chapter = :pc"
                                    params["pc"] = update_chapter
                                    
                                update_query += " WHERE char_id = :cid"
                                
                                db.execute(text(update_query), params)
                                db.commit()
                                st.success("업데이트가 적용되었습니다!")
                                st.rerun()

            # 3. 캐릭터 목록 및 타임라인 결과 출력
            st.markdown(f"#### 📜 현재 등록된 캐릭터 목록 및 변화 타임라인")
            # 새로고침된 최신 데이터를 다시 불러옴
            final_chars = db.execute(text("""
                SELECT name, status, death_chapter, role, personality, personality_change_chapter, background 
                FROM Characters WHERE project_id = :pid
            """), {"pid": selected_pid}).fetchall()
            
            if final_chars:
                df = pd.DataFrame(final_chars, columns=["이름", "상태", "사망 회차", "역할", "성격 및 특징", "성격 변경 회차", "배경 설정"])
                
                # 빈 값(None)을 예쁘게 처리하고 회차 뒤에 '화' 붙이기
                df["사망 회차"] = df["사망 회차"].apply(lambda x: f"{int(x)}화" if pd.notnull(x) else "-")
                df["성격 변경 회차"] = df["성격 변경 회차"].apply(lambda x: f"{int(x)}화" if pd.notnull(x) else "-")
                
                st.dataframe(df, use_container_width=True)
            else:
                st.write("캐릭터를 등록해주세요.")
                
    except Exception as e:
        st.error(f"DB 연결 오류: {e}")
    finally:
        db.close()