import argparse, joblib, pandas as pd
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import HistGradientBoostingClassifier

def retrain(loteria, csv_in, model_out):
    df = pd.read_csv(csv_in)
    # filtra apenas a loteria desejada (ex: 15 dezenas = lotofacil)
    if loteria == "lotofacil":
        X = df.index.values.reshape(-1, 1)
        y = df.iloc[:, 2:17].values          # 15 cols
    elif loteria == "megasena":
        X = df.index.values.reshape(-1, 1)
        y = df.iloc[:, 2:8].values           # 6 cols
    elif loteria == "lotomania":
        X = df.index.values.reshape(-1, 1)
        y = df.iloc[:, 2:22].values          # 20 cols
    else:
        raise ValueError("Loteria desconhecida")

    clf = MultiOutputClassifier(HistGradientBoostingClassifier(max_iter=150, random_state=42))
    clf.fit(X, y)
    joblib.dump(clf, model_out)
    print(f"✅ Modelo {loteria} salvo em {model_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--loteria", required=True)
    parser.add_argument("--csv", default="loteria.csv")
    parser.add_argument("--model-out", required=True)
    args = parser.parse_args()
    retrain(args.loteria, args.csv, args.model_out)