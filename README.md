# 🛠️ PlotSmith (플롯스미스)
**웹소설 서사 장치(클리셰) 추천 및 설정 충돌 방지 AI 모듈 (PoC)**

## 📌 프로젝트 개요
창작자가 웹소설을 기획할 때 겪는 아이디어 고갈 및 세계관 설정 붕괴(Continuity Error) 문제를 해결하기 위한 실무형 내러티브 기획 도구입니다. 대규모 서브컬처 메타데이터를 기반으로 최적의 클리셰 조합을 추천하고, 모순되는 설정 충돌을 사전에 경고합니다.

## 📊 사용 데이터셋
* **출처:** MyAnimeList Dataset 2023 (Kaggle)
* **형태:** 총 24,905행, 작품 메타데이터 및 다중 태그(Genres) 문자열 구조

## ⚙️ 주요 기능 (개발 예정)
1. **연관 규칙 학습(Apriori) 기반 클리셰 추천:** 지지도(Support)와 향상도(Lift)를 연산하여 성공적인 서사 조합 도출.
2. **세계관 위계 질서 무결성 검증:** 고유 설정(Entity) 간의 충돌 및 붕괴 위험도 실시간 감지 및 경고.

## 💻 기술 스택
* **Language:** Python
* **Data Processing:** Pandas, Numpy
* **Machine Learning:** Mlxtend (Apriori Algorithm)
* **Visualization:** Matplotlib