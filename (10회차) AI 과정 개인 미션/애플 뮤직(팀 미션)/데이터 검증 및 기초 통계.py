import pandas as pd

# 1. 통합 데이터 로드
file_name = 'dataset/APPLE_MUSIC_TOTAL_MASTER.csv'
try:
    df = pd.read_csv(file_name)
    print(f"✅ '{file_name}' 파일을 성공적으로 로드했습니다.")
except FileNotFoundError:
    print(f"❌ '{file_name}' 파일이 없습니다. 통합 코드를 먼저 실행해 주세요.")
    exit()

# 2. 데이터 무결성 검증 (Validation)
print("\n" + "="*40)
print("🔍 1. 데이터 무결성 검증 리포트")
print("="*40)

# 주요 컬럼 존재 여부 체크 및 결측치 확인
required_cols = ['plan_type', 'artist_name', 'track_title', 'status']
for col in required_cols:
    if col in df.columns:
        null_count = df[col].isnull().sum()
        fill_rate = (1 - (null_count / len(df))) * 100
        print(f"- {col:12} : 데이터 충전율 {fill_rate:6.1f}% (결측치: {null_count}건)")
    else:
        print(f"- ⚠️ {col:12} : 컬럼이 데이터에 존재하지 않습니다!")

# 3. 기초 통계 분석 (Basic Statistics)
print("\n" + "="*40)
print("📊 2. 주요 지표 기초 통계")
print("="*40)

# (1) 요금제별 분포 (plan_type 에러 방지용 로직)
if 'plan_type' in df.columns:
    print("\n[요금제별 사용자 비중]")
    print(df['plan_type'].value_counts(normalize=True) * 100)
else:
    print("\n⚠️ 'plan_type' 컬럼이 없어 요금제 통계를 산출할 수 없습니다.")

# (2) 인기 아티스트 Top 3
if 'artist_name' in df.columns:
    print("\n[인기 아티스트 Top 3]")
    print(df['artist_name'].value_counts().head(3))

# (3) 트랙 재생 시간 요약
if 'duration' in df.columns:
    print("\n[트랙 재생 시간 정보 (초)]")
    print(df['duration'].describe()[['mean', 'min', 'max']])

# 4. 데이터 정제 (날짜 형식 변환)
# 시각화 시 에러를 막기 위해 날짜 컬럼을 미리 변환해둡니다.
if 'start_date' in df.columns:
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')

print("\n" + "="*40)
print("✅ 검증 완료! 이제 시각화를 진행하셔도 좋습니다.")