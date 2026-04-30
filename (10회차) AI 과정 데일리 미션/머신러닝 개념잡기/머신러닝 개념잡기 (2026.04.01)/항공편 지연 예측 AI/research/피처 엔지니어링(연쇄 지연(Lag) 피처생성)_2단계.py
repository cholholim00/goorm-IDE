import pandas as pd
import numpy as np
import os

def create_lag_features(df):
    print("✈️ 항공기별 연쇄 지연(Lag) 피처 생성 중...")
    # 1. 항공기 번호와 시간순으로 정렬 (직전 비행을 찾기 위해 필수!)
    df = df.sort_values(by=['Tail_Number', 'Month', 'Day_of_Month', 'Estimated_Departure_Time'])
    
    # 2. 직전 비행의 지연 여부(Delay_Target)를 한 칸씩 아래로 밀어서 가져옴
    # groupby('Tail_Number')를 써야 '다른 비행기'의 기록이 섞이지 않습니다.
    df['Prev_Flight_Delay'] = df.groupby('Tail_Number')['Delay_Target'].shift(1).fillna(-1)
    
    return df

# 실행부
try:
    if os.path.exists("최적화/train_step1.pkl"):
        print("📂 1단계 데이터를 불러오는 중...")
        train = pd.read_pickle("최적화/train_step1.pkl")
        
        # 2단계 핵심 로직 적용
        train = create_lag_features(train)
        
        print("\n✅ 2단계 완료! 결과 샘플:")
        print(train[['Tail_Number', 'Month', 'Day_of_Month', 'Delay_Target', 'Prev_Flight_Delay']].head(10))
        
        # 최종 결과 저장
        train.to_pickle("최적화/train_final.pkl")
        print("\n💾 모든 피처가 포함된 'train_final.pkl' 저장 완료!")
    else:
        print("❌ 'train_step1.pkl' 파일이 없습니다. 1단계를 먼저 실행해 주세요.")

except Exception as e:
    print(f"❌ 에러 발생: {e}")