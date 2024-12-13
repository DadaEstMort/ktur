import pandas as pd

def longest_element_lengths(file_path):
    """
    Charge un fichier CSV et renvoie la longueur de l'élément le plus long de chaque colonne.
    
    Paramètres:
        file_path (str): Chemin vers le fichier CSV.

    Retourne:
        dict: Un dictionnaire avec les noms des colonnes comme clés et les longueurs maximales des éléments comme valeurs.
    """
    # Charger le fichier CSV
    df = pd.read_csv("cleaned_data.csv",low_memory=False)

    # Dictionnaire pour stocker la longueur maximale de chaque colonne
    max_lengths = {}

    # Parcourir chaque colonne
    for column in df.columns:
        # Calculer la longueur de chaque élément dans la colonne, en ignorant les NaN
        max_length = df[column].dropna().astype(str).apply(len).max()
        max_lengths[column] = max_length

    return max_lengths

# Chemin vers le fichier CSV
file_path = "votre_fichier.csv"
result = longest_element_lengths(file_path)

# Afficher les résultats
for column, length in result.items():
    print(f"Colonne '{column}': Longueur maximale de {length}")
