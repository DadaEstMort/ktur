import pandas as pd

# Nom des fichiers d'entrée et de sortie
input_file = "/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_bigboss_book.csv"
output_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/unique_characters.csv'

# Fonction pour nettoyer les noms
def clean_name(name):
    name = name.strip()
    # Vérifie si le premier et le dernier caractère sont des guillemets
    if len(name) > 0 and name[0] == '"':
        # Enlève seulement le premier et le dernier guillemet
        name = name[0:-1]
        name = name.replace('""', '"')
        if name.count('"')%2 != 0:
            print(name)
            name = name[1:]
    return name # Enlève les espaces blancs au début et à la fin

# Charger le fichier CSV
df = pd.read_csv(input_file)

# Liste pour stocker les personnages uniques
characters_set = set()

# Extraire et nettoyer les personnages
for characters_list in df['characters']:
    if pd.notna(characters_list):  # Vérifie si la cellule n'est pas NaN
        characters = [char.strip() for char in characters_list.split(',')]
        characters_set.update(characters)

# Appliquer le nettoyage
cleaned_characters = sorted(characters_set)

# Créer le contenu du fichier de sortie
output_lines = []
output_lines.append('character_name\n')  # Ajouter l'en-tête

# Ajouter les personnages nettoyés
for character in cleaned_characters:
    clean_character = clean_name(character)
    output_lines.append(f'"{clean_character}"\n')  # Écrire chaque personnage nettoyé

print(output_lines)

fichier = open(output_file, "w")
for line in output_lines:
    chaine = clean_name(line)
    if len(chaine) > 0:
        chaine_majuscule = chaine[0].upper() + chaine[1:]
        fichier.write(f"{chaine_majuscule}\n")
fichier.close()

print(f"Fichier CSV des personnages uniques sauvegardé sous : {output_file}")