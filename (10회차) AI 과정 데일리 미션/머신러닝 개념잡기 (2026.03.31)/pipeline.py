import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
import lightgbm as lgb
# 최신 방식의 callback 함수들을 따로 import 합니다.
from lightgbm import early_stopping, log_evaluation
from sklearn.metrics import log_loss

# 1. 데이터 로드
# 경로를 사용자의 환경에 맞게 'dataset/'를 제거하거나 수정하세요.
train = pd.read_csv('dataset/train.csv')
test = pd.read_csv('dataset/test.csv')
sample_submission = pd.read_csv('dataset/sample_submission.csv')

# 전처리를 위해 결합 (target인 type 제외)
all_df = pd.concat([train.drop('type', axis=1), test], axis=0)

# 2. 전처리 - 이상치 보정 (Clipping)
mag_cols = [col for col in all_df.columns if 'Mag' in col]
all_df[mag_cols] = all_df[mag_cols].clip(-500, 500)

# 3. 피처 엔지니어링
# (1) 색지수 생성
mag_types = ['psfMag', 'fiberMag', 'petroMag', 'modelMag']
filters = ['u', 'g', 'r', 'i', 'z']
for mt in mag_types:
    for i in range(len(filters)-1):
        all_df[f'{mt}_{filters[i]}-{filters[i+1]}'] = all_df[f'{mt}_{filters[i]}'] - all_df[f'{mt}_{filters[i+1]}']

# (2) 측정 방식 간 차이 생성
for f in filters:
    all_df[f'psf_model_diff_{f}'] = all_df[f'psfMag_{f}'] - all_df[f'modelMag_{f}']

# 불필요한 열 제거 및 데이터 분리
X = all_df[:len(train)].drop(['id', 'fiberID'], axis=1)
X_test = all_df[len(train):].drop(['id', 'fiberID'], axis=1)

# 타겟 레이블링
le = LabelEncoder()
y = le.fit_transform(train['type'])

# 4. 교차 검증 및 모델 학습 (Stratified K-Fold)
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
oof_preds = np.zeros((len(X), len(le.classes_)))
test_preds = np.zeros((len(X_test), len(le.classes_)))

lgb_params = {
    'objective': 'multiclass',
    'num_class': len(le.classes_),
    'metric': 'multi_logloss',
    'learning_rate': 0.01,
    'n_estimators': 5000,
    'max_depth': 9,
    'num_leaves': 64,
    'random_state': 42,
    'n_jobs': -1,
    'force_col_wise': True,
    'verbose': -1 # 훈련 도중 나오는 불필요한 경고 숨김
}

for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    model = lgb.LGBMClassifier(**lgb_params)
    
    # 수정된 fit 방식: callbacks 리스트 활용
    model.fit(
        X_train, y_train, 
        eval_set=[(X_val, y_val)],
        callbacks=[
            early_stopping(stopping_rounds=50),
            log_evaluation(period=100)
        ]
    )

    oof_preds[val_idx] = model.predict_proba(X_val)
    test_preds += model.predict_proba(X_test) / skf.n_splits
    print(f"Fold {fold+1} Completed.")

# 5. 결과 제출 양식 생성
submission = pd.DataFrame(test_preds, columns=le.classes_)
submission.insert(0, 'id', test['id'].values)
submission.to_csv('dataset/hana_final_submission.csv', index=False)
print("제출 파일 'hana_final_submission.csv'이 성공적으로 생성되었습니다.")

# 마지막 Fold의 모델 기준 중요도 시각화
plt.figure(figsize=(10, 12))
lgb.plot_importance(model, max_num_features=30)
plt.title("Feature Importance (Top 30)")
plt.show()