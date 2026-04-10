import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 경로 설정
MODEL_PATH = '모델/flight_delay_high_performance.cbm'
TRAIN_DATA_PATH = 'dataset/train.csv'

model = CatBoostClassifier()
model.load_model(MODEL_PATH)
train_df = pd.read_csv(TRAIN_DATA_PATH)

# --- [추가] 데이터 실제 값 확인 ---
print("전체 데이터 개수:", len(train_df))
print("Delay 컬럼의 실제 값 종류:\n", train_df['Delay'].value_counts(dropna=False))
# ------------------------------

# 2. 전처리 (학습 시와 동일하게)
if 'Estimated_Departure_Time' in train_df.columns:
    train_df['Estimated_Departure_Time_Hour'] = train_df['Estimated_Departure_Time'] // 100
    train_df['Estimated_Departure_Time_Hour_Sin'] = np.sin(2 * np.pi * train_df['Estimated_Departure_Time_Hour'] / 24)
    train_df['Estimated_Departure_Time_Hour_Cos'] = np.cos(2 * np.pi * train_df['Estimated_Departure_Time_Hour'] / 24)

if 'Prev_Flight_Delay' not in train_df.columns:
    train_df['Prev_Flight_Delay'] = 0

# 3. 에러 방지를 위한 동적 라벨 변환
# 문자열(Delayed / Not_Delayed)인 경우 숫자로 매핑
label_map = {'Not_Delayed': 0, 'Delayed': 1, 0: 0, 1: 1, 0.0: 0, 1.0: 1}
train_df['Delay_Numeric'] = train_df['Delay'].map(label_map)

# 정답이 확실히 있는 데이터만 남기기
eval_df = train_df.dropna(subset=['Delay_Numeric']).copy()

if len(eval_df) == 0:
    print("❌ 오류: 평가할 수 있는 데이터(정답이 있는 행)가 0개입니다.")
    print("데이터의 'Delay' 컬럼 내용을 확인해 주세요.")
else:
    trained_features = model.feature_names_
    X_eval = eval_df[trained_features]
    y_true = eval_df['Delay_Numeric'].astype(int)

    # 4. 예측 수행
    y_pred = model.predict(X_eval)
    
    # CatBoost 결과가 문자열일 경우 숫자로 강제 변환
    y_pred_numeric = []
    for p in y_pred:
        try:
            val = int(float(p[0] if isinstance(p, (list, np.ndarray)) else p))
            y_pred_numeric.append(val)
        except: # 문자열로 나올 경우 매핑
            y_pred_numeric.append(1 if p == 'Delayed' else 0)
    
    y_prob = model.predict_proba(X_eval)[:, 1]

    # 5. 지표 계산 및 출력
    metrics = {
        'Accuracy': accuracy_score(y_true, y_pred_numeric),
        'Precision': precision_score(y_true, y_pred_numeric),
        'Recall': recall_score(y_true, y_pred_numeric),
        'F1-Score': f1_score(y_true, y_pred_numeric),
        'ROC-AUC': roc_auc_score(y_true, y_prob)
    }

    print("\n" + "="*30)
    print("     [모델 상세 성적표]     ")
    print("="*30)
    for name, value in metrics.items():
        print(f"{name:10} : {value:.4f}")
    print("="*30)