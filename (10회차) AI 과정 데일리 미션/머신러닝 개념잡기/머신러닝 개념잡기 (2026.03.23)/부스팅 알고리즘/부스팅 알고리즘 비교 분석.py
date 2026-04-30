import pandas as pd
import time
import os
import re  # 특수문자 제거를 위해 추가
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# 1. 파일 경로 설정
train_path = 'dataset/train.csv'
test_path = 'dataset/test.csv'

if not os.path.exists(train_path):
    print(f"❌ 파일을 찾을 수 없습니다.")
else:
    print("✅ 데이터를 불러오는 중입니다...")
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    # 🚨 [중요] LightGBM 특수문자 에러 해결: 피처 이름 변경
    # 특수문자를 모두 언더바(_)로 바꾸거나 제거합니다.
    train.columns = [re.sub(r'[^\w\s]', '_', col) for col in train.columns]
    test.columns = [re.sub(r'[^\w\s]', '_', col) for col in test.columns]

    # 전처리
    X_train, y_train = train.drop('Activity', axis=1), train['Activity']
    X_test, y_test = test.drop('Activity', axis=1), test['Activity']

    le = LabelEncoder()
    y_train_enc = le.fit_transform(y_train)
    y_test_enc = le.transform(y_test)

    # 2. 모델 리스트 (n_jobs=1 설정 유지)
    models = [
        ('XGBoost', XGBClassifier(n_estimators=100, random_state=42, n_jobs=1)),
        ('LightGBM', LGBMClassifier(n_estimators=100, random_state=42, n_jobs=1)),
        ('CatBoost', CatBoostClassifier(n_estimators=100, verbose=0, random_state=42))
    ]

    summary = []
    print("\n🚀 알고리즘 비교 학습을 다시 시작합니다.")
    for name, model in models:
        print(f"[{name}] 학습 중...", end=" ", flush=True)
        start = time.time()
        
        # 여기서 오류가 났던 부분이 이제 해결됩니다.
        model.fit(X_train, y_train_enc)
        
        elapsed = time.time() - start
        pred = model.predict(X_test)
        acc = accuracy_score(y_test_enc, pred)
        
        summary.append({'Algorithm': name, 'Accuracy': acc, 'Training Time(s)': elapsed})
        print(f"완료! ({elapsed:.2f}초)")

    print("\n" + "="*50)
    print("📊 부스팅 알고리즘 최종 비교 결과")
    print("="*50)
    print(pd.DataFrame(summary))
    print("="*50)