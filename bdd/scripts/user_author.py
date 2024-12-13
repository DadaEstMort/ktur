import pandas as pd

author_file_path = "CSV_Author_clean.csv"
user_file_path = "user.csv"

author_df = pd.read_csv(author_file_path, low_memory=False)
user_df = pd.read_csv(user_file_path, low_memory=False)

required_author_columns = {'id_author'}
required_user_columns = {'id_user'}

if not required_author_columns.issubset(author_df.columns):
    raise ValueError(f"Les colonnes {required_author_columns} sont manquantes dans 'CSV_Author_clean.csv'")
if not required_user_columns.issubset(user_df.columns):
    raise ValueError(f"Les colonnes {required_user_columns} sont manquantes dans 'user.csv'")

associations = pd.merge(
    genre_df[['id_author']],
    user_df[['id_user']],
    how='cross'
)

associations.to_csv('user_author.csv', index=False)
