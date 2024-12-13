DROP SCHEMA IF EXISTS saebdd cascade;
CREATE SCHEMA saebdd;
SET SCHEMA 'saebdd';

CREATE TABLE Vote (
  id_book INTEGER,
  id_genre INTEGER,
  nb_votes VARCHAR,
  PRIAMRY KEY (id_book, id_genre),
  FOREIGN KEY (id_book) REFERENCES Book(id_book),
  FOREIGN KEY (id_genre) REFERENCES Genre(id_genre)
);
