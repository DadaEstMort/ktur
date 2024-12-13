import pandas as pd
from deep_translator import GoogleTranslator

'''

SCRIPT QUI PERMET DE TRADUIRE EN FRANCAIS LES GENRES DU CSV QUI SONT EN ANGLAIS

'''

# Charger le fichier CSV
df = pd.read_csv('listes_genres.csv', encoding='utf-8')

# Fonction pour traduire une colonne
def translate_column(df, column, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated_column = []
    total_rows = len(df[column])
    
    for index, row in enumerate(df[column]):
        try:
            # Afficher la progression
            print(f"Traduction {index + 1}/{total_rows}: {row}")
            
            # Remplacer les tirets par des espaces pour une meilleure traduction
            row_prepared = row.replace('-', ' ')
            translated_row = translator.translate(row_prepared)
            
            # Remettre les tirets après la traduction
            translated_row = translated_row.replace(' ', '-')
            translated_column.append(translated_row)
        except Exception as e:
            print(f"Erreur lors de la traduction de la ligne '{row}': {e}")
            translated_column.append(row)  # Ajouter la ligne non traduite en cas d'erreur
    return translated_column

# Traduire les données
translated_data = translate_column(df, 'genre_name', 'fr')

# Sauvegarder les résultats dans un nouveau fichier CSV
pd.DataFrame(translated_data, columns=['genre_name']).to_csv('listes_genres_translate.csv', index=False)
