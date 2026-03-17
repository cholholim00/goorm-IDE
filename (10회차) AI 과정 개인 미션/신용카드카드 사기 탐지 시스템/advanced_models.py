# train_v2.py
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, classification_report
import preprocessing
import smote_handler
import config

def run_advanced_train():
    # 1. 전처리 데이터 로드
    df = preprocessing.load_and_preprocess()
    
    X = df.drop(config.TARGET_COL, axis=1)
    y = df[config.TARGET_COL]
    
    # 2. 데이터 분할 (먼저 나누고 Train에만 SMOTE를 적용해야 함!)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE, stratify=y
    )
    
    # 3. SMOTE 적용 (오직 학습 데이터에만!)
    X_train_res, y_train_res = smote_handler.apply_smote(X_train, y_train)
    
    # 4. 모델 학습
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_res, y_train_res)
    
    # 5. 성능 평가
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    auprc = average_precision_score(y_test, y_pred_prob)
    
    print(f"\n🔥 [이상 탐지] SMOTE 적용 결과")
    print(f"Final AUPRC Score: {auprc:.4f}")
    
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    run_advanced_train()