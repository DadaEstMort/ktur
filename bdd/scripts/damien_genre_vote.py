import csv
import pandas as pd
import psycopg2
from psycopg2 import sql

# Step 1: Load data from CSV
input_csv_path = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_bigboss_book.csv'
output_csv_path = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/unique_genres.csv'

# Read the input CSV
df = pd.read_csv(input_csv_path)

# Step 2: Transform genre_and_votes into separate rows
genre_vote_data = []

for _, row in df.iterrows():
    book_id = row['id']
    genre_votes = row['genre_and_votes']

    # Split the genre_and_votes string into individual genres and votes
    genre_votes_list = [genre.strip() for genre in genre_votes.split(',')]
    if genre_votes_list[0] != "Unknown":
        for genre_vote in genre_votes_list:
            genre_name, vote_count = genre_vote.rsplit(' ', 1)
            genre_vote_data.append({'id_book': book_id, 'genre_name': genre_name, 'nb_vote': int(vote_count)})

# Create a DataFrame for the transformed data
transformed_df = pd.DataFrame(genre_vote_data)

# Step 3: Save transformed data to a new CSV
transformed_df.to_csv(output_csv_path, index=False)

# Fonction pour extraire les genres à partir d'une liste de genres séparés par des virgules ou des points-virgules
def extract_genres(genre_string):
    # Sépare les genres par la virgule ou le point-virgule
    genres = genre_string.replace(";", ",").split(",")
    return [genre.strip() for genre in genres if genre.strip()]

# Lire le fichier CSV Big_bossauthors.csv
input_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_Big_boss_authors.csv'
output_file = '/home/etuinfo/dmeur/Documents/SAE/listes_genres.csv'

# Ensemble pour stocker les genres uniques
unique_genres = set()

# Ouvrir le fichier CSV et lire les données
with open(input_file, newline='', encoding='utf-8') as infile:
    csv_reader = csv.DictReader(infile)
    
    # Extraire les genres des colonnes genre_1, genre_2, et author_genres
    for row in csv_reader:
        # Extraire les genres des colonnes genre_1 et genre_2
        if row['genre_1']:
            unique_genres.update(extract_genres(row['genre_1']))
        if row['genre_2']:
            unique_genres.update(extract_genres(row['genre_2']))
        if row['author_genres']:
            unique_genres.update(extract_genres(row['author_genres']))

# Écrire les genres uniques dans un nouveau fichier CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(['genre_name'])  # Écrire l'entête
    for genre in sorted(unique_genres):  # Trier par ordre alphabétique
        csv_writer.writerow([genre])

print(f"Fichier CSV créé : {output_file}")

# Step 3: Save transformed data to a new CSV
transformed_df.to_csv(output_csv_path, index=False)
