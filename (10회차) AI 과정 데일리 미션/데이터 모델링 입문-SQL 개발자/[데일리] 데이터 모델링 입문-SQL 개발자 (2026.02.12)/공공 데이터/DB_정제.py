import pandas as pd
import sqlite3
import os

# 1. DB 파일 접속 (현재 폴더의 seoul_market.db)
db_file = "seoul_market.db"
conn = sqlite3.connect(db_file)

# 2. 유동인구 CSV 파일 읽기 (파일명 확인!)
csv_file = "dataset/서울시 상권분석서비스(길단위인구-상권).csv"

if not os.path.exists(csv_file):
    print(f"❌ 오류: '{csv_file}' 파일이 없습니다. 파일명을 확인해주세요.")
    exit()

print("📂 데이터 읽는 중...")
try:
    df = pd.read_csv(csv_file, encoding='cp949')
except:
    df = pd.read_csv(csv_file, encoding='utf-8')

# 3. 데이터 정제 (교통량 분석용)
print("⚙️ 데이터 정제 중 (시간대 통합 & 주중/주말 계산)...")

# (1) 시간대 통합
df['Traffic_Morning'] = df['시간대_06_11_유동인구_수']
df['Traffic_Afternoon'] = df['시간대_11_14_유동인구_수'] + df['시간대_14_17_유동인구_수']
df['Traffic_Evening'] = df['시간대_17_21_유동인구_수']
df['Traffic_Night'] = df['시간대_21_24_유동인구_수'] + df['시간대_00_06_유동인구_수']

# (2) 주중/주말 평균 계산
df['Traffic_Weekday'] = (
    df['월요일_유동인구_수'] + df['화요일_유동인구_수'] + 
    df['수요일_유동인구_수'] + df['목요일_유동인구_수'] + df['금요일_유동인구_수']
) / 5

df['Traffic_Weekend'] = (df['토요일_유동인구_수'] + df['일요일_유동인구_수']) / 2

# 4. DB에 저장 (Refined_Traffic 테이블 생성)
# 필요한 컬럼만 선택
final_cols = [
    '기준_년분기_코드', '상권_코드', '상권_코드_명', '총_유동인구_수',
    'Traffic_Morning', 'Traffic_Afternoon', 'Traffic_Evening', 'Traffic_Night',
    'Traffic_Weekday', 'Traffic_Weekend'
]
df_refined = df[final_cols].copy()

# 컬럼명 영어로 변경
df_refined.columns = [
    'year_quarter', 'market_code', 'market_name', 'total_traffic',
    'morning_traffic', 'afternoon_traffic', 'evening_traffic', 'night_traffic',
    'weekday_avg', 'weekend_avg'
]

df_refined.to_sql("Refined_Traffic", conn, if_exists="replace", index=False)

print("✅ 정제 완료! 'Refined_Traffic' 테이블이 생성되었습니다.")
conn.close()