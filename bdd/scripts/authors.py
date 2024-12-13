import pandas as pd
import re

# Nom des fichiers d'entrée et du fichier de sortie
input_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_Big_boss_authors.csv'
output_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/liste_authors.csv'

# Lire le fichier CSV d'entrée
df = pd.read_csv(input_file, quotechar='"', quoting=1)

df = df.drop_duplicates(subset=['author_id'])

# Initialiser une liste pour stocker les données transformées
data = []

# Fonction pour nettoyer les chaînes de texte
def clean_text(text):
    if text:
        text = text.strip()  # Supprimer les espaces en début et fin de chaîne
        text = re.sub(r'\s+', ' ', text)  # Remplacer les espaces multiples par un seul espace
    return text

# Remplir la liste 'data' avec les informations des livres
for idx, row in df.iterrows():
    data.append({
        'author_id': row['author_id'],
        'author_name': clean_text(row['author_name']),  # Appliquer la fonction de nettoyage sur le nom de l'auteur
        'author_gender': clean_text(row['author_gender']),  # Appliquer la fonction de nettoyage sur le genre
        'birthplace': clean_text(row['birthplace']),  # Appliquer la fonction de nettoyage sur le lieu de naissance
        'author_average_rating': row['author_average_rating']
    })

# Traitement supplémentaire pour gérer les virgules dans les noms et lieux
for row in data:
    if ',' in row['author_name']:
        row['author_name'] = row['author_name'].split(',', 1)[0].strip()  # Enlever tout après la première virgule
    if ',' in row['birthplace']:
        row['birthplace'] = row['birthplace'].split(',', 1)[0].strip()  # Enlever tout après la première virgule

# Créer un DataFrame pour les données transformées
transformed_df = pd.DataFrame(data)

# Nom du fichier d'entrée et du fichier de sortie
book_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_bigboss_book.csv'

# Lire le fichier CSV des livres
df_books = pd.read_csv(book_file, quotechar='"', quoting=1)

# Initialiser une liste pour stocker les données transformées
data = []

# Extraire les auteurs et leur moyenne de note pour chaque livre
for idx, row in df_books.iterrows():
    authors = row['author'].split(',')  # Découpe les auteurs séparés par des virgules
    for author in authors:
        author = clean_text(author)  # Appliquer le nettoyage sur le nom de l'auteur
        if len(author) > 0:
            data.append({
                'author_name': author,
                'average_rating': row['average_rating']  # Ajoute la note du livre
            })

# Créer un DataFrame à partir de la liste des auteurs et des notes
authors_df = pd.DataFrame(data)

# Calculer la moyenne des évaluations pour chaque auteur (en regroupant par 'author_name')
authors_avg_rating = authors_df.groupby('author_name')['average_rating'].mean().reset_index()

# Arrondir les moyennes de notes à 2 chiffres après la virgule
authors_avg_rating['average_rating'] = authors_avg_rating['average_rating'].round(2)

# Filtrer les auteurs qui sont dans authors_avg_rating mais pas dans transformed_df
authors_to_keep = authors_avg_rating[~authors_avg_rating['author_name'].isin(transformed_df['author_name'])].copy()

# Ajouter les nouvelles colonnes avec les valeurs par défaut
max_author_id = transformed_df['author_id'].max() if not transformed_df.empty else 0  # Calculer l'ID maximum

authors_to_keep.loc[:, 'author_id'] = range(max_author_id + 1, max_author_id + 1 + len(authors_to_keep))  # Générer les IDs des auteurs
authors_to_keep.loc[:, 'author_gender'] = 'Unknown'  # Valeur par défaut pour author_gender
authors_to_keep.loc[:, 'birthplace'] = 'Unknown'  # Valeur par défaut pour birthplace

# Renommer la colonne average_rating en author_average_rating
authors_to_keep.rename(columns={'average_rating': 'author_average_rating'}, inplace=True)

# Trier transformed_df par 'author_id' (ou une autre colonne si nécessaire)
transformed_df = transformed_df.sort_values(by='author_id', ascending=True)

# Concaténer transformed_df et authors_to_keep
final_df = pd.concat([transformed_df, authors_to_keep], ignore_index=True)

# Sauvegarder le DataFrame combiné dans un fichier CSV
final_df.to_csv(output_file, index=False)

print(f"Fichier CSV combiné et trié sauvegardé sous : {output_file}")