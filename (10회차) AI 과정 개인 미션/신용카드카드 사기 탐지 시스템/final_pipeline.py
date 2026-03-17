# final_pipeline.py
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
import preprocessing, smote_handler, evaluator, config, feature_importance
from sklearn.model_selection import train_test_split

def run_hyper_tuning():
    df = preprocessing.load_and_preprocess()
    X = df.drop(config.TARGET_COL, axis=1)
    y = df[config.TARGET_COL]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_train_res, y_train_res = smote_handler.apply_smote(X_train, y_train)

    # 고도화: 하이퍼파라미터 튜닝 대상 설정
    param_grid = {
        'max_depth': [4, 6],
        'learning_rate': [0.01, 0.1],
        'n_estimators': [100, 200]
    }

    print("🚀 하이퍼파라미터 최적화 시작 (시간이 다소 소요될 수 있습니다)...")
    grid = GridSearchCV(XGBClassifier(eval_metric='logloss'), param_grid, cv=3, scoring='average_precision')
    grid.fit(X_train_res, y_train_res)

    best_model = grid.best_estimator_
    y_probs = best_model.predict_proba(X_test)[:, 1]

    # 최적 임계값 적용 및 중요도 시각화
    best_th = evaluator.find_best_threshold(y_test, y_probs)
    feature_importance.plot_importance(best_model, X.columns)

if __name__ == "__main__":
    run_hyper_tuning()