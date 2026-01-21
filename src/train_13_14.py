import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
import joblib

# 1. Carregar CSV
df = pd.read_csv('loteria.csv')

# 2. Criar targets binários (1 a 25)
sorteios = [f'Bola{i}' for i in range(1, 16)]
Y = []

for _, row in df.iterrows():
    sorteadas = row[sorteios].values
    vetor = [1 if d in sorteadas else 0 for d in range(1, 26)]
    Y.append(vetor)

# 3. Feature simples: índice do sorteio
X = [[i] for i in range(len(Y))]

# 4. Treinar modelo
model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
model.fit(X, Y)

# 5. Salvar modelo
joblib.dump(model, 'src/model.pkl')
print("✅ Modelo treinado e salvo em src/model.pkl")