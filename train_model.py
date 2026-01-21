import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
import joblib

# 1. Carregar o CSV
df = pd.read_csv('loteria.csv')

# 2. Criar targets binários (1 se a dezena saiu, 0 caso contrário)
numeros_sorteados = [f'Bola{i}' for i in range(1, 16)]
dezenas = list(range(1, 26))

Y = []
for _, row in df.iterrows():
    sorteadas = row[numeros_sorteados].values
    vetor = [1 if d in sorteadas else 0 for d in dezenas]
    Y.append(vetor)

Y = pd.DataFrame(Y, columns=[f'd{d}' for d in dezenas])

# 3. Feature simples: índice do sorteio
X = [[i] for i in range(len(Y))]

# 4. Treinar modelo multi-output
model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
model.fit(X, Y)

# 5. Salvar modelo
joblib.dump(model, 'model.pkl')
print("✅ Modelo treinado e salvo como model.pkl")