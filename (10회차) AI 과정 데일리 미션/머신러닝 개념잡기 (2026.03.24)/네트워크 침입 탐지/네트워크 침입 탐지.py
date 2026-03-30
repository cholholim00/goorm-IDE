import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.metrics import classification_report

# =================================================================================
# 1단계 - 데이터 로드 및 탐색 (EDA)
# =================================================================================
print("\n--- 1단계 - 데이터 로드 및 탐색 (EDA)시작 ---")
# 1. 데이터 로드
df = pd.read_csv('dataset/Train_data.csv')

# 2. 범주형 변수 처리 (문자 -> 숫자)
le = LabelEncoder()
for col in ['protocol_type', 'service', 'flag']:
    df[col] = le.fit_transform(df[col])

# 3. 타겟 변수 설정 (이상탐지용: normal=1, anomaly=-1 / 분류용: normal=0, anomaly=1)
y_anomaly = df['class'].apply(lambda x: 1 if x == 'normal' else -1)
y_class = df['class'].apply(lambda x: 0 if x == 'normal' else 1)
X = df.drop('class', axis=1)

# 4. 데이터 스케일링 (이상탐지 모델 필수)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("데이터 전처리 완료. 형상(Shape):", X_scaled.shape)

# =================================================================================
# 2단계 - 교차 검증 실습
# =================================================================================
print("\n--- 2단계 - 교차 검증 시작 ---")
# 모델: 가장 안정적인 RandomForest 사용
rf = RandomForestClassifier(n_estimators=50, random_state=42)

# 방식 1: 기본 K-Fold (데이터를 순서대로 혹은 셔플해서 K개로 나눔)
kf = KFold(n_splits=5, shuffle=True, random_state=42)
kf_scores = cross_val_score(rf, X_scaled, y_class, cv=kf)

# 방식 2: Stratified K-Fold (클래스 비율을 유지하며 나눔 - 권장)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
skf_scores = cross_val_score(rf, X_scaled, y_class, cv=skf)

print("\n--- 교차 검증 결과 ---")
print(f"K-Fold 평균 정확도: {kf_scores.mean():.4f}")
print(f"Stratified K-Fold 평균 정확도: {skf_scores.mean():.4f}")

# =================================================================================
# 3단계 - 이상탐지 모델 실습
# =================================================================================
print("\n--- 3단계 - 이상탐지 모델 실습 시작 ---")
# 계산 효율을 위해 10,000개 샘플로 실습
X_sample = X_scaled[:10000]
y_sample = y_anomaly[:10000]

# 실제 데이터 내의 이상치 비율 (contamination 설정용)
outlier_ratio = (y_sample == -1).sum() / len(y_sample)

# 1. Elliptic Envelope (통계 기반 - 타원형 분포 가정)
ee = EllipticEnvelope(contamination=outlier_ratio, random_state=42)
y_pred_ee = ee.fit_predict(X_sample)

# 2. Isolation Forest (구조 기반 - 무작위 분할을 통한 고립)
iso = IsolationForest(contamination=outlier_ratio, random_state=42)
y_pred_iso = iso.fit_predict(X_sample)

# 3. Local Outlier Factor (밀도 기반 - 주변과의 상대적 밀도 비교)
lof = LocalOutlierFactor(contamination=outlier_ratio)
y_pred_lof = lof.fit_predict(X_sample)

# =================================================================================
# 4단계 - 알고리즘별 특징 분류 및 평가
# =================================================================================

print("\n--- 이상 탐지 알고리즘 성능 비교 ---")
labels = ['Anomaly', 'Normal']

print("\n[1] Elliptic Envelope (통계/분포):")
print(classification_report(y_sample, y_pred_ee, target_names=labels))

print("\n[2] Isolation Forest (트리/고립):")
print(classification_report(y_sample, y_pred_iso, target_names=labels))

print("\n[3] Local Outlier Factor (거리/밀도):")
print(classification_report(y_sample, y_pred_lof, target_names=labels))