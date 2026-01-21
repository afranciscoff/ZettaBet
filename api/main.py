from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# ✅ Carrega o novo modelo
model = joblib.load("src/model.pkl")

# ✅ Rota: previsão das 14 dezenas mais prováveis
@app.get("/previsao")
def previsao():
    df = pd.read_csv("loteria.csv")
    ultimo_indice = len(df) - 1
    X_input = [[ultimo_indice]]

    dezenas_probs = []
    for i, clf in enumerate(model.estimators_):
        prob = clf.predict_proba(X_input)[0][1]
        dezenas_probs.append((i + 1, prob))

    top14 = sorted(dezenas_probs, key=lambda x: x[1], reverse=True)[:14]
    top14_numeros = sorted([d[0] for d in top14])

    return {"top_14": top14_numeros}    