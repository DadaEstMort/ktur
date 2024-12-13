import csv
'''

FICHIER QUI PERMET D'AJOUTER DES ID AUX FICHIERS DES GENRES POUR FACILITER LES JOINTURES
GENRE USER

'''
def add_ids_to_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        # Création des objets reader et writer
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Lire l'entête (si présente) et l'écrire dans le fichier de sortie
        header = next(reader)
        header.insert(0, 'id_genre')  # Ajouter 'id_genre' en première position
        writer.writerow(header)

        # Ajouter l'ID en première colonne pour chaque genre
        for index, row in enumerate(reader, start=1):
            new_row = [index] + row  # Placer l'ID en première position
            writer.writerow(new_row)

input_file = 'listes_genres_translate.csv'  
output_file = 'listes_genres_translate_with_ids.csv'  # Fichier de sortie avec les id_genre

add_ids_to_csv(input_file, output_file)
