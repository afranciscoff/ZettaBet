# testa_insert_abs.py  (funcional e corrigido)
# testa_insert_abs.py  (salve na RAIZ)
import os
import importlib.util

db_path = os.path.join(os.path.dirname(__file__), "api", "db.py")
spec = importlib.util.spec_from_file_location("db", db_path)
db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db)

# restante igual

# Executa o insert
try:
    pid = db.insere_palpite(
    dezenas=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    motor_nome="teste-cli",
    motor_versao="v1.0",
    concurso_ref=3593,
    seed=3593,
    metadata={"fonte": "teste"}   # ← use o nome que está na função
    )
    print("✅ id inserido:", pid)
except Exception as e:
    print("❌ Erro ao inserir:", e)