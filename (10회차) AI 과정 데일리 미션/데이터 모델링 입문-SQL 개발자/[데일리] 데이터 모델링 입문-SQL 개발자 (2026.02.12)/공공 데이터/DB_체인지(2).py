import pandas as pd
import sqlite3
import os

# 1. DB 접속
conn = sqlite3.connect("seoul_market.db")

# 2. 다운로드 받은 파일 이름 (여기를 꼭 수정하세요!)
# 예: "CARD_SUBWAY_MONTH_202601.csv"
subway_file = "dataset/CARD_SUBWAY_MONTH_202601.csv" 

# 3. CSV 파일 읽기
try:
    df_subway = pd.read_csv(subway_file, encoding='cp949')
except:
    df_subway = pd.read_csv(subway_file, encoding='utf-8')

print("📂 원본 컬럼명:", df_subway.columns.tolist())

# 4. 분석하기 좋게 컬럼명 변경
# (공공데이터 컬럼명: 사용일자, 노선명, 역명, 승차총승객수, 하차총승객수...)
df_subway.rename(columns={
    '사용일자': 'use_date',
    '노선명': 'line_num',
    '역명': 'station_name',
    '승차총승객수': 'get_on_count',
    '하차총승객수': 'get_off_count'
}, inplace=True)

# 필요한 컬럼만 선택
use_cols = ['use_date', 'line_num', 'station_name', 'get_on_count', 'get_off_count']
df_final = df_subway[use_cols]

# 5. DB에 저장 (테이블명: Subway_Stats)
df_final.to_sql("Subway_Stats", conn, if_exists="replace", index=False)

print(f"✅ 지하철 데이터 {len(df_final)}건 로드 완료!")
print(df_final.head())

conn.close()