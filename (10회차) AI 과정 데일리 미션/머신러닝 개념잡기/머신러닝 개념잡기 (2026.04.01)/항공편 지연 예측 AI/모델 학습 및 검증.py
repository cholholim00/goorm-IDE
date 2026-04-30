import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
import datetime

# 1. 데이터 로드 및 전처리
TRAIN_DATA_PATH = 'dataset/train.csv'
train_df = pd.read_csv(TRAIN_DATA_PATH)

# 정답 데이터 필터링 및 숫자 변환
label_map = {'Not_Delayed': 0, 'Delayed': 1, 0: 0, 1: 1}
train_df['Delay_Numeric'] = train_df['Delay'].map(label_map)
train_df = train_df.dropna(subset=['Delay_Numeric']).copy()

# 피처 엔지니어링 (기존 로직 동일 적용)
def preprocess(df):
    if 'Estimated_Departure_Time' in df.columns:
        df['Estimated_Departure_Time_Hour'] = df['Estimated_Departure_Time'] // 100
        df['Estimated_Departure_Time_Hour_Sin'] = np.sin(2 * np.pi * df['Estimated_Departure_Time_Hour'] / 24)
        df['Estimated_Departure_Time_Hour_Cos'] = np.cos(2 * np.pi * df['Estimated_Departure_Time_Hour'] / 24)
    if 'Prev_Flight_Delay' not in df.columns:
        df['Prev_Flight_Delay'] = 0
    return df

train_df = preprocess(train_df)

# 2. 가중치(Scale Pos Weight) 계산
num_neg = len(train_df[train_df['Delay_Numeric'] == 0]) # 정상
num_pos = len(train_df[train_df['Delay_Numeric'] == 1]) # 지연
scale_weight = num_neg / num_pos

print(f"--- 데이터 비율 분석 ---")
print(f"정상: {num_neg} | 지연: {num_pos}")
print(f"계산된 가중치: {scale_weight:.4f}")

# 3. 모델 정의 및 학습 (가중치 적용)
features = ['Estimated_Departure_Time_Hour_Sin', 'Estimated_Departure_Time_Hour_Cos', 'Prev_Flight_Delay'] # 실제 사용 중인 피처 리스트로 수정 필요
X = train_df[features]
y = train_df['Delay_Numeric'].astype(int)

model = CatBoostClassifier(
    iterations=1000,
    depth=6,
    learning_rate=0.1,
    scale_pos_weight=scale_weight,  # ⭐ 핵심 파라미터
    loss_function='Logloss',
    random_seed=42,
    verbose=100
)

print("\n--- 재학습 시작 ---")
model.fit(X, y)

# 4. 개선된 모델 저장
new_model_path = f'모델/flight_delay_weighted_{datetime.datetime.now().strftime("%m%d")}.cbm'
model.save_model(new_model_path)
print(f"\n✅ 새 모델 저장 완료: {new_model_path}")