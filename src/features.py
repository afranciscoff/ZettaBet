
#### 📁 `src/features.py

import numpy as np
from itertools import combinations

def extrair_features(combo):
    vet = [1 if i in combo else 0 for i in range(1, 26)]
    soma = sum(combo)
    impares = len([x for x in combo if x % 2])
    primos = len([x for x in combo if x in {2, 3, 5, 7, 11, 13, 17, 19, 23}])
    seq = max([len(list(g)) for _, g in groupby(combo, key=lambda x, c=count(): next(c) - x)], default=0)
    grupos = [len([x for x in combo if 5*i < x <= 5*(i+1)]) for i in range(5)]
    ent = -sum([p * np.log2(p + 1e-12) for p in np.bincount(combo, minlength=26)[1:] / 15])
    desv = np.std(combo)
    return vet + [soma, impares, primos, seq] + grupos + [ent, desv]