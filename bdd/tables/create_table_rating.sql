DROP SCHEMA IF EXISTS saebdd cascade;
CREATE SCHEMA saebdd;
SET SCHEMA 'saebdd';

CREATE TABLE Rating (
  id_rating SERIAL PRIMARY KEY,
  id_book INTEGER,
  id_lecteur INTEGER,
  star_number INTEGER,
  FOREIGN KEY (id_book) REFERENCES Book(id_book),
  FOREIGN KEY (id_lecteur) REFERENCES User(id_lecteur)
);
