drop schema if exists sae cascade;
create schema sae;
set schema 'sae';

CREATE TABLE book (
  id_book SERIAL PRIMARY KEY,
  title VARCHAR(50),
  number_of_pages INTEGER,
  date_published DATE,
  original_title VARCHAR(50),
  isbn INTEGER,
  isbn13 INTEGER,
  description VARCHAR(200)
);

CREATE TABLE author (
  id_author SERIAL PRIMARY KEY,
  author_name VARCHAR(50),
  author_gender VARCHAR(50),
  birthplace VARCHAR(50),
  author_average_rating FLOAT
);
