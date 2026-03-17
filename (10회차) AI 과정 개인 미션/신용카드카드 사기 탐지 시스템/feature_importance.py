# feature_importance.py
import matplotlib.pyplot as plt
import pandas as pd

def plot_importance(model, feature_names):
    # 중요도 추출
    importances = model.feature_importances_
    feat_importances = pd.Series(importances, index=feature_names)
    
    # 상위 10개 시각화
    plt.figure(figsize=(10, 6))
    feat_importances.nlargest(10).plot(kind='barh')
    plt.title("Top 10 Important Features for Fraud Detection")
    plt.show()