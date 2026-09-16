import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# 1. 파일 경로 설정
input_path = 'data/raw/anime-dataset-2023.csv'
output_img_path = 'output/top10_tags_barchart_final.png'

# 2. 데이터 불러오기 및 기본 전처리
print("데이터 불러오는 중...")
df = pd.read_csv(input_path)
df = df.dropna(subset=['Genres'])
df = df[df['Score'] != 'UNKNOWN']
df['Score'] = df['Score'].astype(float)

# 3. 데이터 정예화 (Filtering)
# 조건 A: 내러티브 노이즈 제거 (아동용, 단순 성인물 제외)
exclude_genres = ['Kids', 'Hentai']
df = df[~df['Genres'].str.contains('|'.join(exclude_genres), na=False)]

# 조건 B: 대중성 및 퀄리티 검증 (평점 7.2 이상)
df = df[df['Score'] >= 7.2]
print(f"🔥 최종 정예화된 분석용 데이터 수: {len(df)}개")

# 4. 태그 파싱 (리스트 변환)
def parse_genres(text):
    return [genre.strip() for genre in str(text).split(',')]

df['Tags_List'] = df['Genres'].apply(parse_genres)

# 5. 빈도수 계산 및 시각화
print("시각화 이미지 생성 중...")
all_tags = [tag for tags in df['Tags_List'] for tag in tags]
tag_counts = Counter(all_tags)
top_10_tags = dict(tag_counts.most_common(10))

plt.figure(figsize=(10, 6))
plt.bar(top_10_tags.keys(), top_10_tags.values(), color='royalblue', edgecolor='black')
plt.title('Top 10 Genres/Themes (Filtered: Score >= 7.2)', fontsize=14, fontweight='bold')
plt.xlabel('Tags (Genres/Themes)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# 6. 결과물 저장 및 출력
plt.savefig(output_img_path, dpi=300)
print(f"\n[최종 보고서 첨부용 데이터 샘플 5행]")
print(df[['Name', 'Score', 'Genres']].head(5).to_markdown(index=False))
print(f"\n✅ 이미지 저장 완료! '{output_img_path}'를 확인하세요.")