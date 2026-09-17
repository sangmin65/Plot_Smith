import os
import glob
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# 한글 폰트 설정
import platform
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

def generate_jenova_dashboard(data_folder="data", output_folder="output"):
    print(f"📊 AI 창작 보조 데이터 시각화 리포트 생성 중...")
    os.makedirs(output_folder, exist_ok=True)
    
    json_files = glob.glob(os.path.join(data_folder, "*.json"))
    genres = []
    emotions = []
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            if raw_data.get('type') != 'novel':
                continue
                
            # 장르 수집
            genre_list = raw_data.get('genre', ['미상'])
            if genre_list:
                genres.append(genre_list[0])
            
            # 감정(Emotion) 수집
            for unit in raw_data.get('units', []):
                for script in unit.get('story_scripts', []):
                    emotion = script.get('emotion', '')
                    if emotion:
                        emotions.append(emotion)
        except Exception:
            continue

    if not genres and not emotions:
        print("❌ 분석할 데이터가 없습니다. data 폴더에 json 파일을 넣어주세요.")
        return

    # ---------------------------------------------------------
    # 📈 대시보드 그리기 (1x2 Subplot 구조로 두 그래프를 한 장에!)
    # ---------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Plot_Smith v2.0 (Jenova) : 데이터 파이프라인 분석 리포트', fontsize=18, fontweight='bold', y=1.05)

    # 1. 장르별 분포도
    df_genre = pd.DataFrame({'Genre': genres})
    genre_counts = df_genre['Genre'].value_counts().head(7)
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis', ax=axes[0])
    axes[0].set_title('전처리된 데이터의 장르별 분포 (다변수 파싱 증명)', fontsize=14)
    axes[0].set_xlabel('데이터 수 (Count)', fontsize=11)
    axes[0].set_ylabel('장르 (Genre)', fontsize=11)

    # 2. 감정(Emotion) 분포도 (상민 님의 핵심 아이디어!)
    df_emotion = pd.DataFrame({'Emotion': emotions})
    emotion_counts = df_emotion['Emotion'].value_counts().head(10) # 상위 10개 감정
    sns.barplot(x=emotion_counts.values, y=emotion_counts.index, palette='magma', ax=axes[1])
    axes[1].set_title('추출된 캐릭터 핵심 감정선(Emotion) 분포 Top 10', fontsize=14)
    axes[1].set_xlabel('등장 빈도 (Count)', fontsize=11)
    axes[1].set_ylabel('감정 상태 (Emotion)', fontsize=11)

    plt.tight_layout()
    
    # 이미지 저장
    out_path = os.path.join(output_folder, '데이터_분석_대시보드.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✅ 바탕화면급 고화질 리포트 '{out_path}' 생성 완료!")

if __name__ == "__main__":
    generate_jenova_dashboard()