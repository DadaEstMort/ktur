import pandas as pd

# Nom du fichier d'entrée et du fichier de sortie
input_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/cleaned_bigboss_book.csv'
output_file = '/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/unique_publishers.csv'

# Charger le fichier CSV contenant les informations des livres
df = pd.read_csv(input_file)

# Extraire les éditeurs uniques (en supprimant les valeurs manquantes et les doublons)
unique_publishers = df['publisher'].dropna().unique()

# Créer un DataFrame avec les éditeurs uniques
unique_publishers_df = pd.DataFrame(unique_publishers, columns=['nom'])

# Sauvegarder le DataFrame dans un fichier CSV
unique_publishers_df.to_csv(output_file, index=False)

print(f"Fichier CSV des éditeurs uniques sauvegardé sous : {output_file}")
