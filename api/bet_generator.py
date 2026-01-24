# api/bet_generator.py  23-01-2026
import numpy as np
from datetime import datetime
from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).with_name("models") / "lotofacil.pkl"

def load_model():
    return joblib.load(MODEL_PATH)

def build_features(draw_id: int):
    """Substitua pelo seu pipeline real. Exemplo mínimo."""
    return np.array([[draw_id]])

def gera_palpites_lotofacil(draw_id: int, k: int = 1) -> list[list[int]]:
    """
    Retorna k listas de 15 dezenas (1..25) sem tocar no banco.
    """
    model = load_model()
    X = build_features(draw_id)
    probs = np.array([clf.predict_proba(X)[0][1] for clf in model.estimators_])
    probs = probs / probs.sum()

    rng = np.random.default_rng(seed=draw_id)
    jogos = []
    for _ in range(k):
        dezenas = rng.choice(np.arange(1, 26), size=15, replace=False, p=probas)
        jogos.append(sorted(dezenas.tolist()))
    return jogos