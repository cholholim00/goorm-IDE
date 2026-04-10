import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import precision_recall_curve, f1_score, classification_report, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 모델 및 데이터 로드
MODEL_PATH = '모델/flight_delay_weighted_0319.cbm'
TRAIN_DATA_PATH = 'dataset/train.csv'

model = CatBoostClassifier()
model.load_model(MODEL_PATH)
train_df = pd.read_csv(TRAIN_DATA_PATH)

# 2. 전처리 (필터링 포함)
label_map = {'Not_Delayed': 0, 'Delayed': 1, 0: 0, 1: 1}
train_df['Delay_Numeric'] = train_df['Delay'].map(label_map)
eval_df = train_df.dropna(subset=['Delay_Numeric']).copy()

# 피처 생성 (기존 로직 유지)
if 'Estimated_Departure_Time' in eval_df.columns:
    eval_df['Estimated_Departure_Time_Hour'] = eval_df['Estimated_Departure_Time'] // 100
    eval_df['Estimated_Departure_Time_Hour_Sin'] = np.sin(2 * np.pi * eval_df['Estimated_Departure_Time_Hour'] / 24)
    eval_df['Estimated_Departure_Time_Hour_Cos'] = np.cos(2 * np.pi * eval_df['Estimated_Departure_Time_Hour'] / 24)
if 'Prev_Flight_Delay' not in eval_df.columns:
    eval_df['Prev_Flight_Delay'] = 0

X_eval = eval_df[model.feature_names_]
y_true = eval_df['Delay_Numeric'].astype(int)

# 3. 예측 확률 추출
print("--- 최적 임계값 분석 중... ---")
y_prob = model.predict_proba(X_eval)[:, 1]

# 4. 최적 임계값(Threshold) 찾기
precisions, recalls, thresholds = precision_recall_curve(y_true, y_prob)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-9)
best_idx = np.argmax(f1_scores)
best_threshold = thresholds[best_idx]
best_f1 = f1_scores[best_idx]

# 5. 시각화 및 리포트 출력
plt.figure(figsize=(12, 5))

# [왼쪽] Threshold vs F1-Score 곡선
plt.subplot(1, 2, 1)
plt.plot(thresholds, f1_scores[:-1], color='dodgerblue', lw=2)
plt.axvline(best_threshold, color='red', linestyle='--', label=f'Best: {best_threshold:.3f}')
plt.title('Threshold vs F1-Score')
plt.xlabel('Threshold')
plt.ylabel('F1-Score')
plt.legend()

# [오른쪽] 정밀도-재현율 곡선
plt.subplot(1, 2, 2)
plt.plot(recalls, precisions, color='darkorange', lw=2)
plt.title('Precision-Recall Curve')
plt.xlabel('Recall')
plt.ylabel('Precision')

plt.tight_layout()
plt.show()

print("\n" + "="*40)
print(f"🎯 최적 임계값(Best Threshold): {best_threshold:.4f}")
print(f"📈 최대 F1-Score: {best_f1:.4f}")
print(f"📊 AUC Score: {roc_auc_score(y_true, y_prob):.4f}")
print("="*40)

# 최적 임계값 적용 시의 상세 지표
y_pred_final = (y_prob >= best_threshold).astype(int)
print("\n[최적 임계값 적용 후 상세 성적표]")
print(classification_report(y_true, y_pred_final, target_names=['정상', '지연']))