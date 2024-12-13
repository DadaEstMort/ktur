import pandas as pd

genre_file_path = "listes_genres.csv"
user_file_path = "user.csv"

genre_df = pd.read_csv(genre_file_path, low_memory=False)
user_df = pd.read_csv(user_file_path, low_memory=False)

required_genre_columns = {'id_genre'}
required_user_columns = {'id_user'}

if not required_genre_columns.issubset(genre_df.columns):
    raise ValueError(f"Les colonnes {required_genre_columns} sont manquantes dans 'listes_genres.csv'")
if not required_user_columns.issubset(user_df.columns):
    raise ValueError(f"Les colonnes {required_user_columns} sont manquantes dans 'user.csv'")

associations = pd.merge(
    genre_df[['id_genre']],
    user_df[['id_user']],
    how='cross'
)

associations.to_csv('user_genre.csv', index=False)
