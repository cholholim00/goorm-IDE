# smote_handler.py
from imblearn.over_sampling import SMOTE
import config

def apply_smote(X_train, y_train):
    print(f"📊 SMOTE 적용 전 사기 데이터 개수: {sum(y_train == 1)}")
    
    # SMOTE 객체 생성 (재현성을 위해 config의 RANDOM_STATE 사용)
    sm = SMOTE(random_state=config.RANDOM_STATE)
    
    # 데이터 증식 실행
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)
    
    print(f"🚀 SMOTE 적용 후 사기 데이터 개수: {sum(y_train_res == 1)}")
    return X_train_res, y_train_res