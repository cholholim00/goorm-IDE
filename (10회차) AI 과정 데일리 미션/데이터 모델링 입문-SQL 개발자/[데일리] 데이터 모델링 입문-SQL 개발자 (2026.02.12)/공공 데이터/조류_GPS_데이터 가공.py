import pandas as pd
import sqlite3
import numpy as np
from math import radians, cos, sin, asin, sqrt

# ---------------------------------------------------------
# 1. [함수] 지구상 두 점 사이의 거리 구하기 (Haversine Formula)
# ---------------------------------------------------------
def haversine(lon1, lat1, lon2, lat2):
    """
    위도/경도(도 단위)를 받아 두 지점 간의 대원 거리(km)를 반환
    """
    # 1. 도(degree)를 라디안(radian)으로 변환
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # 2. 하버사인 공식
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 지구 반지름 (km)
    return c * r

# ---------------------------------------------------------
# 2. 업로드한 CSV 파일 읽기
# ---------------------------------------------------------
file_name = "dataset/GPS tracking of guanay cormorants.csv" # 파일명 확인!

print("📂 데이터 로드 중...")
try:
    df = pd.read_csv(file_name)
except FileNotFoundError:
    print(f"❌ '{file_name}' 파일이 없습니다. 같은 폴더에 넣어주세요.")
    exit()

# ---------------------------------------------------------
# 3. 데이터 가공 (Processing) ★핵심★
# ---------------------------------------------------------

# (1) 컬럼 이름 변경 (분석하기 쉽게)
# 실제 파일의 컬럼명 -> 내 코드 변수명
df.rename(columns={
    'individual-local-identifier': 'bird_id', # 새 ID
    'timestamp': 'timestamp',                 # 시간
    'location-long': 'longitude',             # 경도
    'location-lat': 'latitude'                # 위도
}, inplace=True)

# (2) 시간 형식 변환 및 정렬
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.sort_values(by=['bird_id', 'timestamp'], inplace=True)

print("⚙️ 이동 경로 계산 중 (시간이 조금 걸릴 수 있습니다)...")

# (3) 이전 위치 가져오기 (Shift)
# 같은 새(bird_id)의 바로 전 시간대 위치를 옆 컬럼에 붙임
df['prev_lat'] = df.groupby('bird_id')['latitude'].shift(1)
df['prev_lon'] = df.groupby('bird_id')['longitude'].shift(1)
df['prev_time'] = df.groupby('bird_id')['timestamp'].shift(1)

# (4) 이동 거리 계산 (km)
# 첫 번째 행은 이전 위치가 없으므로 0 처리
df['dist_km'] = df.apply(
    lambda x: haversine(x['prev_lon'], x['prev_lat'], x['longitude'], x['latitude']) 
    if pd.notnull(x['prev_lat']) else 0, axis=1
)

# (5) 이동 시간 및 속도 계산 (km/h)
df['time_diff_hours'] = (df['timestamp'] - df['prev_time']).dt.total_seconds() / 3600

df['speed_kmh'] = df.apply(
    lambda x: x['dist_km'] / x['time_diff_hours'] if x['time_diff_hours'] > 0 else 0, axis=1
)

# (6) 상태 분류 (휴식 vs 비행)
# 속도가 1km/h 미만이면 쉬고 있는 것으로 간주
df['status'] = df['speed_kmh'].apply(lambda x: 'Resting' if x < 1 else 'Flying')

# ---------------------------------------------------------
# 4. DB 저장
# ---------------------------------------------------------
conn = sqlite3.connect("bird_tracking.db") # 새 데이터베이스 생성

# 보기 좋게 컬럼 정리
final_cols = ['bird_id', 'timestamp', 'latitude', 'longitude', 'dist_km', 'speed_kmh', 'status']
df_final = df[final_cols].copy()

# 데이터 저장 (테이블명: Bird_Movements)
df_final.to_sql("Bird_Movements", conn, if_exists="replace", index=False)

print(f"✅ 가공 완료! {len(df_final)}건의 데이터가 'bird_tracking.db'에 저장되었습니다.")
print(df_final.head()) # 결과 미리보기

conn.close()