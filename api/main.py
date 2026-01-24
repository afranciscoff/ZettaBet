# api/main.py  23-01-2026
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from .bet_generator import gera_palpites_lotofacil
from .db import insere_palpite

app = FastAPI()

# ---------- carrega modelo ----------
model = joblib.load("../model.pkl")   # ← caminho relativo à pasta api

# ---------- schemas ----------
class GenReq(BaseModel):
    draw_id: int
    k: int = 1

# ---------- rotas ----------
@app.post("/lotofacil/generate")
def lotofacil_gerar_palpites(body: GenReq):
    print("[DEBUG] vou gerar", body.k, "jogos")
    try:
        jogos = gera_palpites_lotofacil(body.draw_id, body.k)
    except Exception as e:
        print("[ERRO] geração falhou:", e)
        raise HTTPException(status_code=500, detail="Erro ao gerar palpites")

    print("[DEBUG] jogos gerados:", jogos)

    ids = []
    for idx, dezenas in enumerate(jogos):
        print("[DEBUG] inserindo jogo", idx, dezenas)
        try:
            pid = insere_palpite(
                dezenas=dezenas,
                motor_nome="zetta-ml",
                motor_versao="v1.0",
                concurso_ref=body.draw_id,
                seed=body.draw_id,
                metadata={"draw_id": body.draw_id, "k": body.k}
            )
            ids.append(pid)
            print("[DEBUG] id inserido:", pid)
        except Exception as e:
            print("[ERRO] insert falhou:", e)
            raise HTTPException(status_code=500, detail="Erro ao persistir palpite")

    print("[DEBUG] ids finais:", ids)
    return {
        "concurso": body.draw_id,
        "quantidade": len(jogos),
        "jogos": jogos,
        "palpite_ids": ids
    }


@app.get("/previsao")
def previsao():
    df = pd.read_csv("../loteria.csv")
    idx = len(df) - 1
    X = [[idx]]
    probs = np.array([clf.predict_proba(X)[0][1] for clf in model.estimators_])
    top15 = sorted([(i + 1, p) for i, p in enumerate(probs)], key=lambda x: x[1], reverse=True)[:15]
    return {"top_15": [n for n, _ in top15]}

from pydantic import BaseModel
class LoginReq(BaseModel):
    usuario: str
    senha: str

@app.post("/login")
def login(body: LoginReq):
    # consulta simples (sem hash por enquanto)
    with SessionLocal() as s:
        row = s.execute(
            text("SELECT id FROM usuarios WHERE usuario = :u AND senha = :s AND ativo = true"),
            {"u": body.usuario, "s": body.senha}
        ).first()
        if not row:
            raise HTTPException(401, "Credenciais inválidas ou usuário inativo")
        return {"id": row[0]}