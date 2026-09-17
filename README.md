# Plot_Smith v2.0 (Jenova MVP Engine) 📝

> 웹소설 창작자를 위한 **서사 무결성 QA 엔진 및 다변수 메타데이터 통합 관리 플랫폼**입니다.
> AI Hub 공공데이터 파싱부터 실시간 타임라인 설정 충돌 검증, 캐릭터 도감 버전 관리까지 제공합니다.

---

## 🚀 주요 기능 (Key Features)

### 1. ✍️ 실시간 에디터 검증 (Tab 1)
* 작가가 원고를 입력할 때 백엔드(FastAPI)와 연동하여 실시간으로 문맥을 분석합니다.
* 특정 캐릭터의 사망 여부나 성격 설정과 충돌하는 문장이 입력되면 즉시 에러를 감지하고 경고합니다.

### 2. 🗄️ 대량 원고 일괄 스캐닝 및 타임라인 검증 (Tab 2)
* AI Hub 공공데이터 전처리 파이프라인(ETL)을 통해 MySQL에 적재된 대규모 원고 데이터를 스캔합니다.
* **타임라인 인지 검증:** 캐릭터가 사망한 회차 이후의 챕터에 재등장하는 등의 치명적인 서사 모순을 교차 검증합니다.

### 3. 👥 캐릭터 도감 및 버전 관리 (설정 백과) (Tab 3)
* 다중 프로젝트(작품)별로 등장인물을 동적으로 필터링하여 열람할 수 있습니다.
* 스토리가 전개됨에 따라 인물의 생사 상태(`ALIVE`/`DEAD`)와 성격 변화가 **'몇 화'**에 일어났는지 타임라인(Timeline)으로 기록하고 추적할 수 있습니다.

### 4. 📊 데이터 파이프라인 분석 리포트
* 비정형 JSON 공공데이터에서 장르(`Genre`) 및 감정선(`Emotion`) 등 다변수 메타데이터를 추출합니다.
* 분석된 통계를 바탕으로 고화질 대시보드 이미지(`.png`)를 `output` 폴더에 자동 생성합니다.

---

## 🛠️ 기술 스택 (Tech Stack)
* **Language:** Python 3.10+
* **Backend:** FastAPI, SQLAlchemy
* **Database:** MySQL (Relational Database)
* **Frontend:** Streamlit
* **Visualization:** Matplotlib, Seaborn

---

## ⚙️ 프로젝트 구조 (Project Structure)
```text
Plot_Smith/
├── data/                 # AI Hub 원천 JSON 데이터 보관소
├── output/               # 시각화 대시보드 리포트 이미지 저장소
├── src/
│   ├── app.py            # Streamlit 프론트엔드 인터페이스
│   ├── database.py       # SQLAlchemy DB 연결 세션 설정
│   ├── preprocessing.py  # AI Hub 데이터 ETL 파이프라인
│   └── visualize.py      # 데이터 분석 대시보드 시각화 스크립트
├── database/
│   └── init_schema.sql   # MySQL 통합 스키마 정의서
└── README.md