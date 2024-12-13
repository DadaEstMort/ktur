import pandas as pd
from connection import get_connection

# Nom du fichier d'entrée et du fichier de sortie
input_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_bigboss_book.csv'
output_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/liste_books.csv'

# Lire le fichier CSV d'entrée
df = pd.read_csv(input_file)

# Initialiser une liste pour stocker les données transformées
data = []

# Remplir la liste 'data' avec les informations des livres
for idx, row in df.iterrows():
    data.append({
        'id_book': row['id'],
        'title': row['title'],
        'number_of_pages': row['number_of_pages'],
        'date_published': row['date_published'],
        'original_title': row['original_title'],
        'isbn': row['isbn'],
        'isbn13': row['isbn13'],
        'description': row['description'],
        'publisher': row['publisher'],
        'series': row['series']
    })

# Créer un DataFrame pour les données transformées
transformed_df = pd.DataFrame(data)

# Sauvegarder les données dans un nouveau fichier CSV
transformed_df.to_csv(output_file, index=False)

author_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_Big_boss_authors.csv'

# Lire le fichier CSV d'entrée
df_author = pd.read_csv(author_file)

# Initialiser une liste pour stocker les données transformées
data_author = []

# Remplir la liste 'data' avec les informations des livres
for idx, row in df_author.iterrows():
    data_author.append({
        'id_book': row['book_id'],
        'title': row['book_title'],
        'number_of_pages': row['pages'],
        'date_published': row['publish_date'],
        'original_title': row['book_title'],
        'isbn': "Unknown",
        'isbn13': "Unknown",
        'description': "No description available",
        'publisher': "Unknown",
        'series': "Unknown"
    })

# Créer un DataFrame pour les données transformées
transformed_authors_df = pd.DataFrame(data_author)

# Concaténer transformed_df et authors_to_keep
final_df = pd.concat([transformed_df, transformed_authors_df], ignore_index=True)

# Sauvegarder le DataFrame combiné dans un fichier CSV
final_df.to_csv('/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/liste_booksaaa.csv', index=False)

# Récupérer la connexion à la base de données
conn = get_connection()

if conn is not None:
    # Curseur pour exécuter la requête
    cur = conn.cursor()

    try:
        # Exécuter une requête pour récupérer les données
        cur.execute("SELECT * FROM kturV2.Publisher")

        # Récupérer les résultats de la requête
        data_publisher = cur.fetchall()

        # Obtenir les noms des colonnes
        columns = [desc[0] for desc in cur.description]

        # Créer un DataFrame pandas avec les résultats et les noms de colonnes
        df_publisher = pd.DataFrame(data_publisher, columns=columns)

        # Exécuter une requête pour récupérer les données
        cur.execute("SELECT * FROM kturV2.Serie")

        # Récupérer les résultats de la requête
        data_serie = cur.fetchall()

        # Obtenir les noms des colonnes
        columns = [desc[0] for desc in cur.description]

        # Créer un DataFrame pandas avec les résultats et les noms de colonnes
        df_serie = pd.DataFrame(data_serie, columns=columns)

    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")

    finally:
        # Fermer le curseur et la connexion
        cur.close()
        conn.close()

else:
    print("Impossible de se connecter à la base de données.")

# Effectuer la jointure entre df_publisher et final_df
df_merged = final_df.merge(df_publisher, left_on='publisher', right_on='nom', how='left')

# Effectuer la jointure entre df_publisher et final_df
df_merged = df_merged.merge(df_serie, left_on='series', right_on='serie_name', how='left')

# Supprimer les colonnes 'series' et 'publisher'
df_merged = df_merged.drop(columns=['series', 'publisher', 'serie_name', 'nom'])

# Sauvegarder le DataFrame combiné dans un fichier CSV
df_merged.to_csv(output_file, index=False)

print(f"Fichier CSV combiné et trié sauvegardé sous : {output_file}")
