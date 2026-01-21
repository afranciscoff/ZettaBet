import pandas as pd, joblib, numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# 1) Gera dataset sintético balanceado (exemplo rápido)
X, y = [], []
for _ in range(200_000):
    combo = sorted(np.random.choice(range(1, 26), 15, replace=False))
    acertos = len(set(combo) & set(sorted(np.random.choice(range(1, 26), 15, replace=False))))
    X.append(extrair_features(combo))
    y.append(int(acertos >= 13))   # target 13+

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
clf = XGBClassifier(n_estimators=1500, max_depth=5, learning_rate=0.01, scale_pos_weight=sum(y)/len(y))
clf.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=50, verbose=False)
joblib.dump(clf, "src/model.pkl")