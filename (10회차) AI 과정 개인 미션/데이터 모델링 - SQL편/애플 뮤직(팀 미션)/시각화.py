import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 1. 데이터 로드
df = pd.read_csv('dataset/APPLE_MUSIC_TOTAL_MASTER.csv')

# 2. 한글 폰트 설정 (Mac/Windows 대응)
if platform.system() == 'Darwin': # Mac
    plt.rc('font', family='AppleGothic')
else: # Windows
    plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 시각화 스타일 설정
sns.set_theme(style="whitegrid", font='AppleGothic' if platform.system() == 'Darwin' else 'Malgun Gothic')
apple_red = '#FF2D55' # 애플 뮤직 시그니처 레드

# --- 시각화 1: 요금제 비중 (Pie Chart) ---
plt.figure(figsize=(10, 7))
plan_counts = df['plan_type'].value_counts()
plt.pie(plan_counts, labels=plan_counts.index, autopct='%1.1f%%', 
        colors=[apple_red, '#FF3B30', '#5856D6'], startangle=140, explode=[0.05, 0, 0])
plt.title('📊 [유저 분석] 구독 요금제별 사용자 비중', fontsize=16, pad=20)
plt.savefig('시각화(이미지)/chart_plan_pie.png')
plt.show()

# --- 시각화 2: 아티스트별 플레이리스트 점유율 (Bar Chart) ---
plt.figure(figsize=(12, 6))
artist_rank = df['artist_name'].value_counts().head(5)
sns.barplot(x=artist_rank.values, y=artist_rank.index, color=apple_red)
plt.title('🎵 [인기 분석] 플레이리스트 내 아티스트 점유율 Top 5', fontsize=16, pad=20)
plt.xlabel('포함된 횟수 (Count)')
plt.savefig('시각화(이미지)/chart_artist_rank.png')
plt.show()

# --- 시각화 3: 요금제별 구독 유지 상태 (Stacked Bar) ---
plt.figure(figsize=(10, 6))
status_plan = pd.crosstab(df['plan_type'], df['status'])
status_plan.plot(kind='bar', stacked=True, color=['#34C759', '#FF3B30'], ax=plt.gca())
plt.title('👥 [상태 분석] 요금제별 Active/Canceled 분포', fontsize=16, pad=20)
plt.xticks(rotation=0)
plt.ylabel('사용자 수')
plt.savefig('시각화(이미지)/chart_subscription_status.png')
plt.show()

# --- 시각화 4: 곡 재생 시간 분포 (Histogram) ---
plt.figure(figsize=(10, 6))
sns.histplot(df['duration'], bins=8, kde=True, color=apple_red)
plt.title('⏳ [트랙 분석] 트랙 재생 시간(초) 분포', fontsize=16, pad=20)
plt.xlabel('재생 시간 (초)')
plt.ylabel('트랙 수')
plt.savefig('시각화(이미지)/chart_duration_dist.png')
plt.show()

print("✅ 4개의 시각화 차트가 생성되어 저장되었습니다!")