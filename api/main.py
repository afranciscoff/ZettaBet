from fastapi import FastAPI
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

# ---------- carrega modelo ----------
model = joblib.load("src/model.pkl")   # seu MultiOutputClassifier já treinado

# ---------- schemas ----------
class GenReq(BaseModel):
    draw_id: int
    k: int = 1

# ---------- funções auxiliares ----------
def build_features(draw_id: int):
    """Exemplo mínimo: só o índice do concurso. Substitua pelo seu pipeline real."""
    return np.array([[draw_id]])

# ---------- rotas ----------
@app.post("/lotofacil/generate")
def lotofacil_gerar_palpites(body: GenReq):
    """
    Gera k palpites (15 dezenas) para o concurso draw_id.
    Usa o modelo já carregado para amostrar 15 números entre 1-25.
    """
    X = build_features(body.draw_id)
    # probabilidade de cada dezena (0/1) – média sobre os 25 estimadores
    probs = np.array([clf.predict_proba(X)[0][1] for clf in model.estimators_])
    probs = probs / probs.sum()          # normaliza

    rng = np.random.default_rng(seed=body.draw_id)
    jogos = []
    for _ in range(body.k):
        dezenas = rng.choice(
            np.arange(1, 26), size=15, replace=False, p=probs
        )
        jogos.append(sorted(dezenas.tolist()))

    return {
        "concurso": body.draw_id,
        "quantidade": len(jogos),
        "jogos": jogos
    }

@app.get("/previsao")
def previsao():
    """
    Mantém a rota original, mas agora retorna as 15 dezenas mais prováveis
    (Lotofácil = 15 números, não 14).
    """
    df = pd.read_csv("loteria.csv")
    ultimo_indice = len(df) - 1
    X_input = [[ultimo_indice]]

    dezenas_probs = []
    for i, clf in enumerate(model.estimators_):
        prob = clf.predict_proba(X_input)[0][1]
        dezenas_probs.append((i + 1, prob))

    top15 = sorted(dezenas_probs, key=lambda x: x[1], reverse=True)[:15]
    top15_numeros = sorted([d[0] for d in top15])

    return {"top_15": top15_numeros}