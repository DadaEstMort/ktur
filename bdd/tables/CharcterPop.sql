DROP schema if exists saebdd cascade;
create schema saebdd;
set schema 'saebdd';


CREATE TABLE Character (
  id_character SERIAL PRIMARY KEY,
  id_book INTEGER,
  character_name VARCHAR,
  FOREIGN KEY (id_book) REFERENCES Book(id_book),
  FOREIGN KEY (id_genre) REFERENCES Genre(id_genre)
);

WbImport
-file='/home/etuinfo/gleonplevert/Documents/S5/SAE/Character.csv'
-type=text
-table=Character
-header=true
