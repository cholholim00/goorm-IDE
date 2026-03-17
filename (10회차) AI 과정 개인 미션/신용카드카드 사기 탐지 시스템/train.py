# train.py
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, classification_report
import preprocessing
import config

def run_train():
    # 1. 전처리된 데이터 가져오기
    df = preprocessing.load_and_preprocess()
    
    # 2. 데이터 분할 (Feature와 Label 분리)
    X = df.drop(config.TARGET_COL, axis=1)
    y = df[config.TARGET_COL]
    
    # 불균형 데이터이므로 stratify 옵션 필수
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=config.TEST_SIZE, 
        random_state=config.RANDOM_STATE, 
        stratify=y
    )
    
    # 3. 모델 학습 (Base Line: Logistic Regression)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    
    # 4. 성능 평가
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    auprc = average_precision_score(y_test, y_pred_prob)
    
    print(f"\n🚀 [이상 탐지] 모델 평가 결과")
    print(f"Final AUPRC Score: {auprc:.4f}")
    print("\n[상세 리포트]")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    run_train()