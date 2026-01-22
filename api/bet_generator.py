# models/bet_generator.py
import numpy as np
from sqlalchemy.orm import Session
from app.db import Bet, SessionLocal
from app.ml import load_model, normalize_hits

def generate_games(draw_id: int, k: int = 1, cold_start: bool = False):
    """
    Gera k jogos (palpites) para o concurso draw_id.
    Retorna lista de dicts pronta para inserir na tabela `bets_staging`.
    """
    model = load_model()                       # seu .pkl em /models
    features = build_features(draw_id)         # seu pipeline atual
    probas = model.predict_proba(features)[0]  # vetor 1x25 (ex: 25 dezenas)

    # evita repetir mesma sequência se k>1
    rng = np.random.default_rng(seed=draw_id)

    games = []
    for _ in range(k):
        # sampling ponderado sem reposição
        dezenas = rng.choice(
            np.arange(1, 26),         # 1..25 (ajuste ao seu jogo)
            size=15,                  # qtde dezenas por jogo
            replace=False,
            p=probas / probas.sum()
        )
        games.append(
            dict(
                draw_id=draw_id,
                numbers=sorted(dezenas.tolist()),
                score=normalize_hits(dezenas, probas),  # métrica interna
                generated_at=datetime.utcnow()
            )
        )
    return games