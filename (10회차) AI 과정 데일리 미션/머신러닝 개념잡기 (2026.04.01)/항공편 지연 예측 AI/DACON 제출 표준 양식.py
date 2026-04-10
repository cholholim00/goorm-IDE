import pandas as pd
import numpy as np
from catboost import CatBoostClassifier

# 1. 모델과 데이터 로드
model = CatBoostClassifier()
model.load_model('모델/flight_delay_ULTIMATE.cbm')
test_df = pd.read_csv('dataset/test.csv')
submission = pd.read_csv('dataset/sample_submission.csv') # 원본 양식 로드

# 2. 테스트 데이터 전처리 (학습 시와 동일하게)
test_df['Estimated_Departure_Time_Hour'] = test_df['Estimated_Departure_Time'] // 100
test_df['Estimated_Departure_Time_Hour_Sin'] = np.sin(2 * np.pi * test_df['Estimated_Departure_Time_Hour'] / 24)
test_df['Estimated_Departure_Time_Hour_Cos'] = np.cos(2 * np.pi * test_df['Estimated_Departure_Time_Hour'] / 24)
test_df['Prev_Flight_Delay'] = 0

X_test = test_df[model.feature_names_]

# 3. 확률(Probability) 예측 수행
# [중요] LogLoss/AUC 평가 대회라면 확률값을 제출해야 합니다.
probs = model.predict_proba(X_test)

# 4. 양식에 맞게 확률값 채우기
submission['Not_Delayed'] = probs[:, 0] # 정상 운항 확률
submission['Delayed'] = probs[:, 1]     # 지연 운항 확률

# 5. 최종 파일 저장 (컬럼은 ID, Not_Delayed, Delayed만 남게 됨)
submission.to_csv('dataset/final_submission_Hana_Group_dacon.csv', index=False)

print("✅ 수정된 최종 제출 파일이 생성되었습니다: final_submission_Hana_Group_dacon.csv")
print(submission.head())