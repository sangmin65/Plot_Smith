import pandas as pd

# 1. 데이터 불러오기
input_path = 'data/raw/anime-dataset-2023.csv'
df = pd.read_csv(input_path)

# 2. 전처리 (UNKNOWN 제거 및 숫자형 변환)
df = df[df['Score'] != 'UNKNOWN']
df['Score'] = df['Score'].astype(float)

# 3. 명백한 노이즈 장르(아동용, 단순 성인물) 사전 제거
df = df.dropna(subset=['Genres'])
exclude_genres = ['Kids', 'Hentai']
df = df[~df['Genres'].str.contains('|'.join(exclude_genres), na=False)]

# 4. 평점 커트라인별 데이터 개수 시뮬레이션
print("📊 평점 커트라인별 남은 데이터 개수 시뮬레이션")
for score_cut in [7.8, 7.5, 7.2, 7.0, 6.8]:
    count = len(df[df['Score'] >= score_cut])
    print(f"- 평점 {score_cut} 이상 기준: {count}개")