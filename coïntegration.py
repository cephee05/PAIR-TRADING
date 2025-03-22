import pandas as pd
import numpy as np
from statsmodels.api import OLS, add_constant
from statsmodels.tsa.stattools import adfuller

# Charger les données des deux actifs
fichier1 = 'C:\\Users\\wille\\Desktop\\Statistical Arbitrage\\ETHUSD-1d-26wks-data.csv'  # Actif 1
fichier2 = 'C:\\Users\\wille\\Desktop\\Statistical Arbitrage\\SOLUSD-1d-26wks-data.csv'  # Actif 2
data1 = pd.read_csv(fichier1)
data2 = pd.read_csv(fichier2)

# Convertir datetime en format DateTime
data1['datetime'] = pd.to_datetime(data1['datetime'])
data2['datetime'] = pd.to_datetime(data2['datetime'])

# Fusionner les deux DataFrames sur 'datetime'
data = pd.merge(data1[['datetime', 'Close']], data2[['datetime', 'Close']], on='datetime', suffixes=('_actif1', '_actif2'))

# Extraire les colonnes de prix de clôture
y = data['Close_actif1']  # Série dépendante
x = data['Close_actif2']  # Série indépendante

# Étape 1 : Régression linéaire pour estimer la relation
x = add_constant(x)  # Ajouter une constante
model = OLS(y, x).fit()
residuals = model.resid  # Résidus de la régression

# Étape 2 : Test de stationnarité (ADF test) sur les résidus
adf_test = adfuller(residuals)

# Résultats
print("=== Résultats ===")
print(f"Coefficient de la régression : {model.params}")
print(f"Test ADF (résidus) : Statistique = {adf_test[0]}, p-value = {adf_test[1]}")
if adf_test[1] < 0.05:
    print("Les résidus sont stationnaires. Les séries sont coïntégrées.")
else:
    print("Les résidus ne sont pas stationnaires. Les séries ne sont pas coïntégrées.")
