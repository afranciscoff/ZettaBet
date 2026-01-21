import joblib
import pandas as pd

# 1. Carregar modelo treinado
model = joblib.load('model.pkl')

# 2. Carregar o CSV para saber o índice do último sorteio
df = pd.read_csv('loteria.csv')
ultimo_indice = len(df) - 1  # último sorteio

# 3. Prever probabilidades para cada dezena (1 a 25)
X_input = [[ultimo_indice]]
dezenas_probs = []

for i, clf in enumerate(model.estimators_):
    prob = clf.predict_proba(X_input)[0][1]  # classe 1 = saiu
    dezenas_probs.append((i + 1, prob))

# 4. Ranquear e pegar as top 14 mais prováveis
top14 = sorted(dezenas_probs, key=lambda x: x[1], reverse=True)[:14]
top14_numeros = [d[0] for d in top14]

# 5. Exibir resultado
print("🎯 Top 14 dezenas mais prováveis para o próximo sorteio:")
print("→", sorted(top14_numeros))