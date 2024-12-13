CREATE TABLE serie (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
);

COPY serie(id, name, id_book)
FROM 'serie.csv'
DELIMITER ','
CSV HEADER;
