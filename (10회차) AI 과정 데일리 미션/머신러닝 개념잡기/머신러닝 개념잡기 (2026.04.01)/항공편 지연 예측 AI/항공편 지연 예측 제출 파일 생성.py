import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
import datetime

# 1. 경로 설정
DATA_PATH = 'dataset/'
MODEL_PATH = '모델/flight_delay_high_performance.cbm'

# 2. 데이터 및 모델 로드
test_df = pd.read_csv(f'{DATA_PATH}test.csv')
sample_submission = pd.read_csv(f'{DATA_PATH}sample_submission.csv')
model = CatBoostClassifier()
model.load_model(MODEL_PATH)

print("--- 피처 엔지니어링 시작 ---")

# [중요] 에러 해결: 학습 시와 동일한 전처리를 수행해야 합니다.
# 아래는 에러 메시지에 기반한 예시 로직입니다. 학습 코드의 전처리 부분을 확인해 보세요.

# 예시 1: 시간 데이터(Estimated_Departure_Time)에서 Hour 추출 및 주기성 변환
# (원본 데이터 형식이 HHMM 형태라고 가정할 때)
if 'Estimated_Departure_Time' in test_df.columns:
    test_df['Estimated_Departure_Time_Hour'] = test_df['Estimated_Departure_Time'] // 100
    
    # 주기성 피처 생성 (Sin/Cos)
    test_df['Estimated_Departure_Time_Hour_Sin'] = np.sin(2 * np.pi * test_df['Estimated_Departure_Time_Hour'] / 24)
    test_df['Estimated_Departure_Time_Hour_Cos'] = np.cos(2 * np.pi * test_df['Estimated_Departure_Time_Hour'] / 24)

# 예시 2: Prev_Flight_Delay (이전 항공편 지연 여부) 생성
# 학습 시 이 값을 어떻게 만드셨는지 확인이 필요합니다. (예: 특정 ID별 직전 결과 등)
if 'Prev_Flight_Delay' not in test_df.columns:
    # 학습 시 결측치 처리 방식에 따라 0이나 특정 값으로 채워야 할 수 있습니다.
    test_df['Prev_Flight_Delay'] = 0 

# 3. 모델이 요구하는 피처만 선택
trained_features = model.feature_names_

# 여기서 다시 한번 체크: 전처리 후에도 없는 컬럼이 있는지 확인
missing_cols = set(trained_features) - set(test_df.columns)
if missing_cols:
    print(f"⚠️ 여전히 다음 컬럼이 부족합니다: {missing_cols}")
    # 부족한 컬럼은 학습 시의 기본값(0 등)으로 임시 생성하거나 전처리 로직을 추가해야 합니다.
    for col in missing_cols:
        test_df[col] = 0

X_test = test_df[trained_features]

# 4. 예측 및 저장
probs = model.predict_proba(X_test)[:, 1]
sample_submission['Delay'] = probs

timestamp = datetime.datetime.now().strftime('%m%d_%H%M')
sample_submission.to_csv(f'{DATA_PATH}submission_{timestamp}.csv', index=False)

print(f"제출 파일 생성 완료: submission_{timestamp}.csv")