import pandas as pd
import numpy as np
from scipy.stats import zscore

# Charger les deux fichiers CSV
fichier1 = 'C:\\Users\\wille\\Desktop\\ARBITRAGE\\BTCUSD-1d-4wks-data.csv'  # Chemin vers le fichier 1
fichier2 = 'C:\\Users\\wille\\Desktop\\ARBITRAGE\\XRPUSD-1d-4wks-data.csv'  # Chemin vers le fichier 2

data1 = pd.read_csv(fichier1)
data2 = pd.read_csv(fichier2)

# Vérifier les premières lignes des fichiers
print("Aperçu des données Actif 1 :")
print(data1.head())
print("\nAperçu des données Actif 2 :")
print(data2.head())

# Aligner les deux fichiers sur la colonne 'datetime'
data1['datetime'] = pd.to_datetime(data1['datetime'])
data2['datetime'] = pd.to_datetime(data2['datetime'])

# Fusionner les deux DataFrames sur la colonne 'datetime'
data_merged = pd.merge(data1, data2, on='datetime', suffixes=('_actif1', '_actif2'))

# Calculer le spread normalisé (normalisation statistique)
mean_actif1 = data_merged['Close_actif1'].mean()
std_actif1 = data_merged['Close_actif1'].std()
mean_actif2 = data_merged['Close_actif2'].mean()
std_actif2 = data_merged['Close_actif2'].std()

data_merged['Close_actif1_norm'] = (data_merged['Close_actif1'] - mean_actif1) / std_actif1
data_merged['Close_actif2_norm'] = (data_merged['Close_actif2'] - mean_actif2) / std_actif2

data_merged['Spread_Normalise'] = data_merged['Close_actif1_norm'] - data_merged['Close_actif2_norm']

# Calculer la moyenne du spread normalisé
spread_normalise_mean = data_merged['Spread_Normalise'].mean()

# Calculer l'écart-type (standard deviation) du spread normalisé
spread_normalise_std = data_merged['Spread_Normalise'].std()

# Calculer la variance du spread normalisé (variance = std²)
spread_normalise_variance = spread_normalise_std**2

# Évaluation de la stabilité du spread normalisé
if spread_normalise_std < 1:  # Ajustez le seuil selon vos besoins
    stability_message = "Le spread normalisé est stable autour de sa moyenne (faible écart-type)."
else:
    stability_message = "Le spread normalisé est instable (fort écart-type)."

# Calculer les rendements logarithmiques pour chaque actif
data_merged['Return_Close_Actif1'] = np.log(data_merged['Close_actif1'] / data_merged['Close_actif1'].shift(1))
data_merged['Return_Close_Actif2'] = np.log(data_merged['Close_actif2'] / data_merged['Close_actif2'].shift(1))

# Supprimer les lignes avec des valeurs manquantes (première ligne des rendements)
data_merged = data_merged.dropna()

# Calculer la corrélation entre les rendements des deux actifs
correlation = data_merged['Return_Close_Actif1'].corr(data_merged['Return_Close_Actif2'])

# Calcul du Z-score pour le spread normalisé
z_scores = zscore(data_merged['Spread_Normalise'])
data_merged['Z_Score'] = z_scores

# Vérifier si les Z-scores sortent de l'intervalle [-1.96, 1.96]
significant_z_scores = data_merged[(data_merged['Z_Score'] < -1.96) | (data_merged['Z_Score'] > 1.96)]

print("=== Résultats ===")
print(f"\nCorrélation entre les rendements des deux actifs : {correlation}")
print(f"Moyenne du Spread Normalisé : {spread_normalise_mean}")
print(f"Écart-Type du Spread Normalisé : {spread_normalise_std}")
print(f"Variance du Spread Normalisé : {spread_normalise_variance}")
print(stability_message)
print(f"Nombre de Z-scores significatifs (en dehors de [-1.96, 1.96]) : {len(significant_z_scores)}")
