import pandas as pd
import csv

# Nom des fichiers d'entrée et de sortie
authors_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_Big_boss_authors.csv'  # Fichier des auteurs
books_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_bigboss_book.csv'  # Fichier des livres
output_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/unique_genres.csv'  # Fichier de sortie pour les genres uniques

# Fonction pour extraire les genres à partir d'une liste de genres séparés par des virgules ou des points-virgules
def extract_genres(genre_string):
    # Sépare les genres par la virgule ou le point-virgule
    genres = genre_string.replace(";", ",").split(",")
    return [genre.strip() for genre in genres if genre.strip()]

# Fonction pour appliquer une règle de casse (majuscule initiale et après espace ou tiret, sans espace ajouté)
def format_case(genre_name):
    formatted = []
    for part in genre_name.split('-'):  # Gérer les mots séparés par des tirets
        formatted.append(' '.join(word.capitalize() for word in part.split()))
    return '-'.join(formatted)  # Réassemble avec des tirets sans espaces

# Charger les fichiers CSV
authors_df = pd.read_csv(authors_file)
books_df = pd.read_csv(books_file)

# Ensemble pour stocker les genres uniques
unique_genres = set()

# Extraire les genres des colonnes 'genre_1', 'genre_2', et 'author_genres' des auteurs
for _, row in authors_df.iterrows():
    if pd.notna(row['genre_1']):
        unique_genres.update(extract_genres(row['genre_1']))
    if pd.notna(row['genre_2']):
        unique_genres.update(extract_genres(row['genre_2']))
    if pd.notna(row['author_genres']):
        unique_genres.update(extract_genres(row['author_genres']))

# Extraire les genres des livres dans 'genre_and_votes' et les ajouter à l'ensemble
for _, row in books_df.iterrows():
    genre_votes = row['genre_and_votes']
    if pd.notna(genre_votes) and genre_votes != "Unknown":
        # Split the genre_and_votes string into individual genres and votes
        genre_votes_list = [genre.strip() for genre in genre_votes.split(',')]
        for genre_vote in genre_votes_list:
            genre_name, _ = genre_vote.rsplit(' ', 1)  # Extraire le nom du genre (avant le nombre de votes)
            unique_genres.add(genre_name.strip())

# Appliquer la règle de casse sur tous les genres
formatted_genres = {format_case(genre) for genre in unique_genres}

# Sauvegarder les genres uniques formatés dans un fichier CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(['genre_name'])  # Écrire l'entête
    for genre in formatted_genres:  # Trier par ordre alphabétique
        csv_writer.writerow([genre])

print(f"Fichier CSV des genres uniques sauvegardé sous : {output_file}")
