import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
import datetime

# 1. 초기 설정
MODEL_PATH = '모델/flight_delay_weighted_0319.cbm' # 방금 만든 가중치 모델
TRAIN_DATA_PATH = 'dataset/train.csv'
features = ['Estimated_Departure_Time_Hour_Sin', 'Estimated_Departure_Time_Hour_Cos', 'Prev_Flight_Delay']

# 2. 데이터 로드 및 전처리 함수
def preprocess(df):
    df = df.copy()
    if 'Estimated_Departure_Time' in df.columns:
        df['Estimated_Departure_Time_Hour'] = df['Estimated_Departure_Time'] // 100
        df['Estimated_Departure_Time_Hour_Sin'] = np.sin(2 * np.pi * df['Estimated_Departure_Time_Hour'] / 24)
        df['Estimated_Departure_Time_Hour_Cos'] = np.cos(2 * np.pi * df['Estimated_Departure_Time_Hour'] / 24)
    if 'Prev_Flight_Delay' not in df.columns:
        df['Prev_Flight_Delay'] = 0
    return df

train_df = pd.read_csv(TRAIN_DATA_PATH)
label_map = {'Not_Delayed': 0, 'Delayed': 1, 0: 0, 1: 1}

# 정답 있는 데이터(Labeled)
labeled_df = train_df.dropna(subset=['Delay']).copy()
labeled_df['Delay_Numeric'] = labeled_df['Delay'].map(label_map)
labeled_df = preprocess(labeled_df)

# 정답 없는 데이터(Unlabeled)
unlabeled_df = train_df[train_df['Delay'].isna()].copy()
unlabeled_df = preprocess(unlabeled_df)

# 3. Pseudo-Labeling 수행
print("--- 기존 모델로 결측치 예측 시작 ---")
model = CatBoostClassifier()
model.load_model(MODEL_PATH)
probs = model.predict_proba(unlabeled_df[features])[:, 1]

# 확신이 매우 높은 데이터만 추출 (임계값 0.9 / 0.1)
unlabeled_df['Delay_Numeric'] = -1
unlabeled_df.loc[probs >= 0.90, 'Delay_Numeric'] = 1 # 지연 확신
unlabeled_df.loc[probs <= 0.10, 'Delay_Numeric'] = 0 # 정상 확신

pseudo_labeled = unlabeled_df[unlabeled_df['Delay_Numeric'] != -1].copy()
print(f"새롭게 추가된 학습 데이터: {len(pseudo_labeled)}건")

# 4. 데이터 합치기 (Original + Pseudo)
final_train_df = pd.concat([labeled_df, pseudo_labeled], axis=0)

# 5. 최종 ULTIMATE 모델 학습
print(f"\n--- 최종 통합 데이터({len(final_train_df)}건) 학습 시작 ---")
X_final = final_train_df[features]
y_final = final_train_df['Delay_Numeric'].astype(int)

# 불균형은 여전하므로 scale_pos_weight는 유지합니다
num_neg = len(final_train_df[final_train_df['Delay_Numeric'] == 0])
num_pos = len(final_train_df[final_train_df['Delay_Numeric'] == 1])
final_scale_weight = num_neg / num_pos

ultimate_model = CatBoostClassifier(
    iterations=1000,
    depth=6,
    scale_pos_weight=final_scale_weight,
    random_seed=42,
    verbose=100
)

ultimate_model.fit(X_final, y_final)

# 6. 저장
final_path = '모델/flight_delay_ULTIMATE.cbm'
ultimate_model.save_model(final_path)
print(f"\n✅ 최종 모델 저장 완료: {final_path}")