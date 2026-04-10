import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# 1. 경로 및 모델 설정
DATA_PATH = 'dataset/'
MODEL_PATH = '모델/flight_delay_high_performance.cbm'

# 한글 폰트 설정 (Mac 기준, Windows라면 'Malgun Gothic' 사용)
plt.rcParams['font.family'] = 'AppleGothic' 
plt.rcParams['axes.unicode_minus'] = False

print("--- 데이터 및 모델 로딩 시작 ---")

# 2. 로드 및 전처리
test_df = pd.read_csv(f'{DATA_PATH}test.csv')
sample_submission = pd.read_csv(f'{DATA_PATH}sample_submission.csv')

model = CatBoostClassifier()
model.load_model(MODEL_PATH)

# [피처 엔지니어링] 이전 단계에서 해결한 로직을 반드시 포함해야 합니다.
if 'Estimated_Departure_Time' in test_df.columns:
    test_df['Estimated_Departure_Time_Hour'] = test_df['Estimated_Departure_Time'] // 100
    test_df['Estimated_Departure_Time_Hour_Sin'] = np.sin(2 * np.pi * test_df['Estimated_Departure_Time_Hour'] / 24)
    test_df['Estimated_Departure_Time_Hour_Cos'] = np.cos(2 * np.pi * test_df['Estimated_Departure_Time_Hour'] / 24)

if 'Prev_Flight_Delay' not in test_df.columns:
    test_df['Prev_Flight_Delay'] = 0

# 모델 학습 시 사용된 피처 순서대로 정렬
trained_features = model.feature_names_
X_test = test_df[trained_features]

# 3. 예측 수행
probs = model.predict_proba(X_test)[:, 1]
sample_submission['Delay'] = probs

# 4. 시각화 (Feature Importance & Distribution)
print("--- 시각화 리포트 생성 중 ---")
feature_importance = model.get_feature_importance()
fi_df = pd.DataFrame({'Feature': trained_features, 'Importance': feature_importance}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(12, 10))

# [그래프 1] Feature Importance
plt.subplot(2, 1, 1)
sns.barplot(x='Importance', y='Feature', data=fi_df.head(15), palette='magma')
plt.title('모델의 핵심 예측 변수 (Top 15 Feature Importance)')

# [그래프 2] Probability Distribution
plt.subplot(2, 1, 2)
sns.histplot(probs, bins=50, kde=True, color='teal')
plt.axvline(x=0.5, color='red', linestyle='--', label='Default Threshold (0.5)')
plt.title('전체 항공편 지연 확률 분포')
plt.xlabel('지연 확률')
plt.legend()

plt.tight_layout()
plt.show()

# 5. 결과 저장
timestamp = datetime.datetime.now().strftime('%m%d_%H%M')
sample_submission.to_csv(f'{DATA_PATH}submission_{timestamp}.csv', index=False)

print(f"\n[최종 요약]")
print(f"- 가장 중요한 변수: {fi_df.iloc[0]['Feature']}")
print(f"- 파일 저장 완료: submission_{timestamp}.csv")