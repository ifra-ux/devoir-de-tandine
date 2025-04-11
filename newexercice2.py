
import pandas as pd
from itertools import combinations
from collections import Counter

# Charger les données
file_path = r"C:\Users\Hp\Downloads\all_data_2025.csv"
data = pd.read_csv(file_path)

# Afficher les colonnes disponibles pour vérification
print("Colonnes disponibles :", data.columns)

# Nettoyer les données
data = data[data['Order Date'] != 'Order Date']  # Supprimer les en-têtes mal placés
data = data.dropna(subset=['Order Date'])  # Supprimer les lignes avec des valeurs manquantes

# Convertir la colonne 'Order Date' en datetime
data['Order Date'] = pd.to_datetime(data['Order Date'], format='%m/%d/%y %H:%M', errors='coerce')
data = data.dropna(subset=['Order Date'])  # Supprimer les lignes avec des dates invalides

# Convertir les colonnes 'Quantity Ordered' et 'Price Each' en nombres
data['Quantity Ordered'] = pd.to_numeric(data['Quantity Ordered'], errors='coerce')
data['Price Each'] = pd.to_numeric(data['Price Each'], errors='coerce')
data = data.dropna(subset=['Quantity Ordered', 'Price Each'])  # Supprimer les lignes avec des valeurs non valides

# Extraire le mois et la ville
data['Mois'] = data['Order Date'].dt.to_period('M')  # Extraire le mois
data['Ville'] = data['Purchase Address'].str.split(',').str[1].str.strip()  # Extraire la ville

# Calculer le chiffre d'affaires par ligne
data['Chiffre_affaires'] = data['Quantity Ordered'] * data['Price Each']

# 1. Chiffre d'affaires par produit, mois et ville
resultats = data.groupby(['Product', 'Mois', 'Ville'])['Chiffre_affaires'].sum().reset_index()

# 2. Produits les plus souvent achetés ensemble
commandes = data.groupby('Order ID')['Product'].apply(list)
paires_produits = Counter()
for produits in commandes:
    produits.sort()  # Trier pour éviter les doublons (A+B et B+A)
    paires_produits.update(combinations(produits, 2))  # Compter les paires
produits_plus_achetes_ensemble = paires_produits.most_common(1)[0][0]  # Paire la plus fréquente

# Ajouter les produits les plus souvent achetés ensemble aux résultats
resultats['Produits_achetes_ensemble'] = f"{produits_plus_achetes_ensemble[0]} et {produits_plus_achetes_ensemble[1]}"

# Enregistrer les résultats dans un fichier CSV
resultats.to_csv('resultats_organises.csv', index=False)

# Afficher les résultats à l'écran
print("Résultats organisés par produit, mois, ville et chiffre d'affaires :")
print(resultats)

print("\nProduits les plus souvent achetés ensemble :")
print(f"{produits_plus_achetes_ensemble[0]} et {produits_plus_achetes_ensemble[1]}")