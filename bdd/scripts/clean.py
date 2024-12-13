import pandas as pd
import os
import re

# Chemins des fichiers CSV
path_book = "/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/bigboss_book.csv"
path_author = "/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/Big_boss_authors.csv"

# Fonction pour nettoyer les espaces et caractères invisibles
def clean_csv(file_path, keep_columns=None):
    try:
        if not os.path.exists(file_path):
            print(f"Fichier introuvable : {file_path}")
            return None

        # Charger le fichier CSV dans un DataFrame
        df = pd.read_csv(file_path)

        # Supprimer les espaces au début et à la fin des valeurs dans chaque colonne
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Remplacer les doubles espaces par un seul espace dans toutes les colonnes du DataFrame
        df = df.applymap(lambda x: ' '.join(x.split()) if isinstance(x, str) else x)

        # Considérer les valeurs composées uniquement d'espaces ou vides comme NaN
        df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)

        # Conserver uniquement les colonnes spécifiées si nécessaire
        if keep_columns is not None:
            df = df.iloc[:, :keep_columns]

        # Extraire l'année des colonnes 'publish_date' et 'date_published'
        for col in ['publish_date', 'date_published']:
            if col in df.columns:
                # Tenter de convertir les colonnes en dates et extraire uniquement l'année
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.year

                # Remplacer les NaN (valeurs manquantes) par 0 ou une autre valeur par défaut
                df[col].fillna(0, inplace=True)

                # Forcer la conversion en entier (int)
                df[col] = df[col].astype(int)

        # Forcer la colonne 'number_of_pages' en entier (int)
        if 'number_of_pages' in df.columns:
            df['number_of_pages'] = pd.to_numeric(df['number_of_pages'], errors='coerce')
            df['number_of_pages'] = df['number_of_pages'].fillna(0).astype(int)

        # Remplacer les virgules par des points dans les colonnes contenant "average" dans le nom
        for column in df.columns:
            if "average" in column.lower():  # Vérifier que "average" est dans le nom de la colonne
                # Remplacer les virgules par des points dans les chaînes de caractères
                df[column] = df[column].astype(str).str.replace(',', '.', regex=False)

                # Convertir la colonne en float après le remplacement
                df[column] = pd.to_numeric(df[column], errors='coerce')

        # Nettoyage spécifique de la colonne 'series'
        if 'series' in df.columns:
            # Supprimer tous les caractères après le premier `#`, y compris ce caractère
            df['series'] = df['series'].apply(lambda x: re.findall(r'^.(.*)#.*$', str(x))[0] if re.findall(r'^.(.*)#.*$', str(x)) else x)

        if 'description' in df.columns:
            # Remplacer les virgules par des points dans les chaînes de caractères
            df['description'] = df['description'].str.replace(',', '', regex=False)
        
        return df
    except Exception as e:
        print(f"Erreur lors du nettoyage du fichier {file_path} : {e}")
        return None

# Fonction pour analyser les valeurs manquantes dans un DataFrame
def analyze_missing_values(df, file_description):
    if df is None:
        print(f"Impossible d'analyser les valeurs manquantes pour {file_description} car le DataFrame est vide ou inexistant.")
        return

    # Calculer le nombre et le pourcentage de valeurs manquantes par colonne
    missing_values = df.isnull().sum()
    total_rows = len(df)
    missing_percentage = (missing_values / total_rows) * 100

    # Afficher les résultats
    print(f"\nAnalyse des valeurs manquantes pour : {file_description}")
    print(f"{'Colonne':<30} {'Valeurs Manquantes':<20} {'Pourcentage (%)':<15}")
    print("-" * 70)
    for column, missing, percentage in zip(df.columns, missing_values, missing_percentage):
        print(f"{column:<30} {missing:<20} {percentage:<15.2f}")

# Fonction pour traiter les valeurs manquantes
def handle_missing_values(df, defaults):
    """
    Remplace les valeurs manquantes dans un DataFrame selon les valeurs par défaut spécifiées.

    :param df: DataFrame à traiter
    :param defaults: Dictionnaire avec {colonne: valeur_par_defaut}
    :return: DataFrame avec les valeurs manquantes traitées
    """
    for column, default_value in defaults.items():
        if column in df.columns:
            # Remplacer les valeurs manquantes par la valeur par défaut
            df[column] = df[column].apply(lambda x: default_value if pd.isna(x) or (isinstance(x, str) and x.strip() == '') else x)

            # Si 'publish_date' ou 'date_published' contient 0, les remplacer par la valeur par défaut
            if column in ['publish_date', 'date_published']:
                df[column] = df[column].replace(0, default_value)

    return df

# Définir les valeurs par défaut pour les colonnes manquantes
defaults_books = {
    "series": "Unknown",
    "number_of_pages": 0,
    "date_published": "Unknown",
    "publisher": "Unknown",
    "original_title": "Unknown",
    "genre_and_votes": "Unknown",
    "isbn": "Unknown",
    "isbn13": "Unknown",
    "settings": "Unknown",
    "characters": "Unknown",
    "awards": "None",
    "books_in_series": "Unknown",
    "description": "No description available"
}

defaults_authors = {
    "birthplace": "Unknown",
    "publish_date": "Unknown"
}

# Nettoyage des fichiers
cleaned_book = clean_csv(path_book, keep_columns=24)
cleaned_author = clean_csv(path_author)

# Traiter les valeurs manquantes
if cleaned_book is not None:
    cleaned_book = handle_missing_values(cleaned_book, defaults_books)
    print("Valeurs manquantes traitées pour les livres.")

if cleaned_author is not None:
    cleaned_author = handle_missing_values(cleaned_author, defaults_authors)
    print("Valeurs manquantes traitées pour les auteurs.")

# Sauvegarde après traitement
if cleaned_book is not None:
    cleaned_book.to_csv("/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_bigboss_book.csv", index=False)
    print("Fichier des books avec valeurs manquantes traitées sauvegardé sous 'cleaned_bigboss_book.csv'.")

if cleaned_author is not None:
    cleaned_author.to_csv("/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_Big_boss_authors.csv", index=False)
    print("Fichier des auteurs avec valeurs manquantes traitées sauvegardé sous 'cleaned_Big_boss_authors.csv'.")

# Analyse des valeurs manquantes
analyze_missing_values(cleaned_book, "Books")
analyze_missing_values(cleaned_author, "Authors")
