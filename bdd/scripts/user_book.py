import pandas as pd

book_file_path = "books_for_import.csv"
user_file_path = "user.csv"

book_df = pd.read_csv(author_file_path, low_memory=False)
user_df = pd.read_csv(user_file_path, low_memory=False)

required_book_columns = {'id_book'}
required_user_columns = {'id_user'}

if not required_book_columns.issubset(book_df.columns):
    raise ValueError(f"Les colonnes {required_book_columns} sont manquantes dans 'books_for_import.csv'")
if not required_user_columns.issubset(user_df.columns):
    raise ValueError(f"Les colonnes {required_user_columns} sont manquantes dans 'user.csv'")

associations = pd.merge(
    genre_df[['id_book']],
    user_df[['id_user']],
    how='cross'
)

associations.to_csv('user_book.csv', index=False)
