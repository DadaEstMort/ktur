DROP SCHEMA IF EXISTS saebdd cascade;
CREATE SCHEMA saebdd;
SET SCHEMA 'saebdd';

CREATE TABLE Character (
  id_character SERIAL PRIMARY KEY,
  id_book INTEGER,
  character_name VARCHAR,
  FOREIGN KEY (id_book) REFERENCES Book(id_book),
  FOREIGN KEY (id_genre) REFERENCES Genre(id_genre)
);
