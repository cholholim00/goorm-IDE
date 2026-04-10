import pandas as pd
import numpy as np

def safe_reduce_mem_usage(df):
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        c_min, c_max = df[col].min(), df[col].max()
        if pd.api.types.is_integer_dtype(df[col]):
            if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                df[col] = df[col].astype(np.int8)
            else:
                df[col] = df[col].astype(np.int32)
        else:
            df[col] = df[col].astype(np.float32)
    return df

def process_time_features(df):
    print("⏰ 시간 데이터 Cyclic Encoding 적용 중...")
    for col in ['Estimated_Departure_Time', 'Estimated_Arrival_Time']:
        # 결측치는 -1로 임시 대체
        df[col] = df[col].fillna(-1)
        
        # 시간/분 분리 (1030.0 -> 10시 30분)
        df[f'{col}_Hour'] = df[col].apply(lambda x: x // 100 if x != -1 else -1)
        df[f'{col}_Minute'] = df[col].apply(lambda x: x % 100 if x != -1 else -1)
        
        # Cyclic Encoding: 23시와 0시가 가깝다는 것을 수학적으로 표현
        # 결측치(-1)인 경우는 그대로 -1 혹은 0으로 두어 모델이 구분하게 함
        df[f'{col}_Hour_Sin'] = np.where(df[f'{col}_Hour'] != -1, 
                                         np.sin(2 * np.pi * df[f'{col}_Hour'] / 24), -1)
        df[f'{col}_Hour_Cos'] = np.where(df[f'{col}_Hour'] != -1, 
                                         np.cos(2 * np.pi * df[f'{col}_Hour'] / 24), -1)
    return df

try:
    # 1. 데이터 로드 및 최적화
    print("🚀 데이터 로딩 및 메모리 최적화 시작...")
    train = pd.read_csv('dataset/train.csv')
    train = safe_reduce_mem_usage(train)

    # 2. 시간 피처 처리
    train = process_time_features(train)

    # 3. 타겟 변수 수치화 (Delayed: 1, Not_Delayed: 0, NaN: -1)
    print("🎯 타겟 변수 수치화 진행 중...")
    target_map = {'Not_Delayed': 0, 'Delayed': 1}
    train['Delay_Target'] = train['Delay'].map(target_map).fillna(-1).astype(np.int8)

    print("\n✅ 피처 엔지니어링 1단계 완료!")
    print(train[['Estimated_Departure_Time_Hour', 'Estimated_Departure_Time_Hour_Sin', 'Delay_Target']].head())
    
    # 결과 확인을 위한 샘플 출력
    print(f"\n변환 후 데이터 크기: {train.shape}")

except Exception as e:
    print(f"❌ 에러 발생: {e}")
    
# 1단계 결과 저장 (데이터가 크니 용량이 작은 pickle 권장)
train.to_pickle("최적화/train_step1.pkl")
print("💾 1단계 결과가 'train_step1.pkl'로 저장되었습니다.")