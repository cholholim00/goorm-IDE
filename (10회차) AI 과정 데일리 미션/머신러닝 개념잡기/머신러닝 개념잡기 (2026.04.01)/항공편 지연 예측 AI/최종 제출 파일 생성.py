import pandas as pd
import numpy as np
from catboost import CatBoostClassifier

# 1. 환경 설정
MODEL_PATH = '모델/flight_delay_ULTIMATE.cbm' # 또는 weighted_0319
DATA_PATH = 'dataset/'

# 2. 모델 및 테스트 데이터 로드
model = CatBoostClassifier()
model.load_model(MODEL_PATH)
test_df = pd.read_csv(f'{DATA_PATH}test.csv')
submission = pd.read_csv(f'{DATA_PATH}sample_submission.csv')

# 3. 전처리 (학습 시와 동일한 로직 필수!)
test_df['Estimated_Departure_Time_Hour'] = test_df['Estimated_Departure_Time'] // 100
test_df['Estimated_Departure_Time_Hour_Sin'] = np.sin(2 * np.pi * test_df['Estimated_Departure_Time_Hour'] / 24)
test_df['Estimated_Departure_Time_Hour_Cos'] = np.cos(2 * np.pi * test_df['Estimated_Departure_Time_Hour'] / 24)
test_df['Prev_Flight_Delay'] = 0 # 추론 단계 기본값

# 모델이 학습한 피처 순서대로 추출
X_test = test_df[model.feature_names_]

# 4. 예측 (최적 임계값 적용)
# 아까 리포트에서 확인한 F1-Score가 가장 높았던 임계값을 사용하세요.
# 만약 잘 모르겠다면, 가중치 모델의 성격상 '0.4866'이 적당한 기준이 됩니다.
probs = model.predict_proba(X_test)[:, 1]
best_th = 0.4866 
submission['Delay'] = (probs >= best_th).astype(int)

# 5. 최종 저장
output_name = f'final_submission_Hana_Group.csv'
submission.to_csv(f'{DATA_PATH}{output_name}', index=False)

print(f"🎉 모든 과정 완료! 최종 파일이 생성되었습니다: {output_name}")