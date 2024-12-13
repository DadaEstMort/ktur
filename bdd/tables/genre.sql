CREATE TABLE genre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    id_author INTEGER NOT NULL,
    id_book INTEGER NOT NULL,
);
