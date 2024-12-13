import pandas as pd

genre_file_path = "genre.csv"
genre_df = pd.read_csv(genre_file_path, low_memory=False)

author_file_path = "author.csv"
author_df = pd.read_csv(author_file_path, low_memory=False)

associations = []

for index, genre_row in genre_df.iterrows():
    genre_name = genre_row['genre']
    for author_index, author_row in author_df.iterrows():
        id_author = author_row['id_author']
        associations.append({'id_genre': genre_row['id_genre'], 'id_author': id_author})

filtered_df = pd.DataFrame(associations)

filtered_df.to_csv('genre_author.csv', index=False)
