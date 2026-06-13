import pandas as pd
import numpy as np
import multiprocessing
from math import radians, cos, sin, asin, sqrt
import time
import os

# ---------------------------------------------------------
# 1. 공통 함수: 거리 계산 (Haversine)
# ---------------------------------------------------------
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

# ---------------------------------------------------------
# 2. [Map 단계] 개별 CPU 코어가 처리할 작업 정의
# (입력: "특정 새 1마리"의 데이터 조각)
# ---------------------------------------------------------
def process_bird_chunk(bird_chunk):
    bird_id = bird_chunk['bird_id'].iloc[0]
    # print(f"🦅 일꾼(프로세스)가 '{bird_id}'의 경로를 계산 중입니다...")
    
    # 시간순 정렬
    bird_chunk = bird_chunk.sort_values('timestamp')
    
    # 이전 위치 계산
    bird_chunk['prev_lat'] = bird_chunk['latitude'].shift(1)
    bird_chunk['prev_lon'] = bird_chunk['longitude'].shift(1)
    bird_chunk['prev_time'] = bird_chunk['timestamp'].shift(1)
    
    # 거리 계산
    bird_chunk['dist_km'] = bird_chunk.apply(
        lambda x: haversine(x['prev_lon'], x['prev_lat'], x['longitude'], x['latitude']) 
        if pd.notnull(x['prev_lat']) else 0, axis=1
    )
    
    # 속도 및 상태 계산
    bird_chunk['time_diff_hours'] = (bird_chunk['timestamp'] - bird_chunk['prev_time']).dt.total_seconds() / 3600
    bird_chunk['speed_kmh'] = bird_chunk.apply(
        lambda x: x['dist_km'] / x['time_diff_hours'] if x['time_diff_hours'] > 0 else 0, axis=1
    )
    bird_chunk['status'] = bird_chunk['speed_kmh'].apply(lambda x: 'Resting' if x < 1 else 'Flying')
    
    return bird_chunk

# ---------------------------------------------------------
# 3. 메인 실행부 (MapReduce 오케스트레이션)
# ---------------------------------------------------------
# ★중요★ 파이썬 병렬처리는 반드시 if __name__ == '__main__': 안에 써야 합니다.
if __name__ == '__main__':
    file_name = "GPS tracking of guanay cormorants.csv"
    
    if not os.path.exists(file_name):
        print(f"❌ '{file_name}' 파일이 없습니다.")
        exit()

    print("📂 전체 데이터를 불러오는 중...")
    df = pd.read_csv(file_name)
    df.rename(columns={
        'individual-local-identifier': 'bird_id',
        'timestamp': 'timestamp',
        'location-long': 'longitude',
        'location-lat': 'latitude'
    }, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # ---------------------------------------------------------
    # [데이터 분할] 새(bird_id) 별로 데이터를 쪼갭니다.
    # ---------------------------------------------------------
    unique_birds = df['bird_id'].dropna().unique()
    # 각 새의 데이터를 담은 리스트 생성 (이 리스트를 일꾼들에게 나눠줄 겁니다)
    chunks = [df[df['bird_id'] == bird].copy() for bird in unique_birds]
    
    print(f"🔪 총 {len(unique_birds)}마리의 새 데이터로 쪼갰습니다.")
    
    start_time = time.time()
    
    # 사용할 수 있는 CPU 코어 수 확인
    cores = multiprocessing.cpu_count()
    print(f"🚀 {cores}개의 CPU 코어를 풀가동하여 병렬 처리를 시작합니다!\n")
    
    # ---------------------------------------------------------
    # [Map & Reduce] 병렬 처리 실행 및 결과 병합
    # ---------------------------------------------------------
    # 1. Pool 생성 (고용할 일꾼 수)
    with multiprocessing.Pool(processes=cores) as pool:
        # 2. Map: 쪼갠 데이터(chunks)를 process_bird_chunk 함수에 던져서 동시 계산
        processed_chunks = pool.map(process_bird_chunk, chunks)
        
    # 3. Reduce: 각 코어에서 계산이 끝난 조각들을 다시 하나의 표로 뭉칩니다. (pd.concat)
    final_df = pd.concat(processed_chunks, ignore_index=True)
    
    end_time = time.time()
    
    print("✅ MapReduce 병렬 처리 완료!")
    print(f"⏱️ 소요 시간: {end_time - start_time:.2f}초")
    
    # 결과 확인을 위해 필요한 컬럼만 추출
    final_cols = ['bird_id', 'timestamp', 'dist_km', 'speed_kmh', 'status']
    print("\n📊 최종 병합된 데이터 미리보기:")
    print(final_df[final_cols].head())
    
    # 필요하다면 DB나 CSV로 다시 저장
    # final_df[final_cols].to_csv("Processed_Bird_GPS.csv", index=False)