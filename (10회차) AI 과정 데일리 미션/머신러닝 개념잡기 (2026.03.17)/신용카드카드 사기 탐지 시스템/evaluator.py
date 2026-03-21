# evaluator.py
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
import numpy as np

def find_best_threshold(y_test, y_probs):
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)
    
    # F1-Score가 최대가 되는 지점 찾기
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-9)
    best_idx = np.argmax(f1_scores)
    best_threshold = thresholds[best_idx]
    
    print(f"🎯 최적의 임계값(Threshold): {best_threshold:.4f}")
    print(f"📈 해당 지점의 Precision: {precisions[best_idx]:.4f}, Recall: {recalls[best_idx]:.4f}")
    
    return best_threshold