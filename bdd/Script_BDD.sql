drop schema if exists kturV2 cascade ;
create schema kturV2;

CREATE TABLE kturV2.User (
    id_lecteur SERIAL PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    birthdate DATE,
    gender VARCHAR(10),
    profession VARCHAR(255)
);

CREATE TABLE kturV2.Publisher (
    id_publisher SERIAL PRIMARY KEY,
    nom VARCHAR(255)
);

CREATE TABLE kturV2.Serie (
    id_serie SERIAL PRIMARY KEY,
    serie_name VARCHAR(255)
);


CREATE TABLE kturV2.Book (
    id_book INT PRIMARY KEY,
    title VARCHAR(255),
    number_of_pages INT,
    date_published INT,
    original_title VARCHAR(255),
    isbn VARCHAR(20),
    isbn13 VARCHAR(20),
    description TEXT,
    id_publisher INT,
    id_serie INT NULL,
    FOREIGN KEY (id_publisher) REFERENCES kturV2.Publisher(id_publisher),
    FOREIGN KEY (id_serie) REFERENCES kturV2.Serie(id_serie)
);

CREATE TABLE kturV2.Genre (
    id_genre SERIAL PRIMARY KEY,
    genre_name VARCHAR(255)
);

CREATE TABLE kturV2.Vote (
    nb_vote INTEGER NOT NULL,
    id_genre INTEGER NOT NULL REFERENCES kturV2.Genre(id_genre),
    id_book INTEGER NOT NULL REFERENCES kturV2.Book(id_book),
    primary key (id_genre, id_book)
);

CREATE TABLE kturV2.Author (
    author_id INT PRIMARY KEY,
    author_name VARCHAR(255),
    author_gender VARCHAR(10),
    birthplace VARCHAR(255),
    author_average_rating FLOAT
);

CREATE TABLE kturV2.Character (
    id_character SERIAL PRIMARY KEY,
    character_name VARCHAR(255)
);

CREATE TABLE kturV2.Setting (
    id_setting SERIAL PRIMARY KEY,
    setting_name VARCHAR(255)
);

CREATE TABLE kturV2.Award (
    id_award SERIAL PRIMARY KEY,
    award_name VARCHAR(255),
    award_year INT
);

CREATE TABLE kturV2.Review (
    id_review SERIAL PRIMARY KEY,
    id_lecteur INT,
    id_book INT,
    review_text VARCHAR(255),
    FOREIGN KEY (id_lecteur) REFERENCES kturV2.User(id_lecteur),
    FOREIGN KEY (id_book) REFERENCES kturV2.Book(id_book)
);

CREATE TABLE kturV2.Rating (
    id_rating SERIAL PRIMARY KEY,
    id_lecteur INT,
    id_book INT,
    star_number INT,
    FOREIGN KEY (id_lecteur) REFERENCES kturV2.User(id_lecteur),
    FOREIGN KEY (id_book) REFERENCES kturV2.Book(id_book)
);

-- Relations "many-to-many" avec des tables de jointure
CREATE TABLE kturV2.Book_Genre (
    id_book INT,
    id_genre INT,
    PRIMARY KEY (id_book, id_genre),
    FOREIGN KEY (id_book) REFERENCES kturV2.Book(id_book),
    FOREIGN KEY (id_genre) REFERENCES kturV2.Genre(id_genre)
);

CREATE TABLE kturV2.Book_Author (
    id_book INT,
    author_id INT,
    PRIMARY KEY (id_book, author_id),
    FOREIGN KEY (id_book) REFERENCES kturV2.Book(id_book),
    FOREIGN KEY (author_id) REFERENCES kturV2.Author(author_id)
);

CREATE TABLE kturV2.Book_Character (
    id_book INT,
    id_character INT,
    PRIMARY KEY (id_book, id_character),
    FOREIGN KEY (id_book) REFERENCES kturV2.Book(id_book),
    FOREIGN KEY (id_character) REFERENCES kturV2.Character(id_character)
);

CREATE TABLE kturV2.Book_Setting (
    id_book INT,
    id_setting INT,
    PRIMARY KEY (id_book, id_setting),
    FOREIGN KEY (id_book) REFERENCES kturV2.Book(id_book),
    FOREIGN KEY (id_setting) REFERENCES kturV2.Setting(id_setting)
);

CREATE TABLE kturV2.Book_Award (
    id_book INT,
    id_award INT,
    PRIMARY KEY (id_book, id_award),
    FOREIGN KEY (id_book) REFERENCES kturV2.Book(id_book),
    FOREIGN KEY (id_award) REFERENCES kturV2.Award(id_award)
);

-- Table de jointure pour la relation "User - Book" (a lu)
CREATE TABLE kturV2.User_Book (
    id_lecteur INT,
    id_book INT,
    PRIMARY KEY (id_lecteur, id_book),
    FOREIGN KEY (id_lecteur) REFERENCES kturV2.User(id_lecteur),
    FOREIGN KEY (id_book) REFERENCES kturV2.Book(id_book)
);

-- Table de jointure pour la relation "Genre - Author" (a lu)
CREATE TABLE kturV2.Genre_Author (
    id_genre INT,
    id_author INT,
    PRIMARY KEY (id_genre, id_author),
    FOREIGN KEY (id_genre) REFERENCES kturV2.Genre(id_genre),
    FOREIGN KEY (id_author) REFERENCES kturV2.Author(author_id)
);

CREATE TABLE kturV2.User_Genre (
    id_lecteur INT,
    id_book INT,
    id_genre INT,
    PRIMARY KEY (id_lecteur, id_genre),
    FOREIGN KEY (id_lecteur) REFERENCES kturV2.User(id_lecteur),
    FOREIGN KEY (id_genre) REFERENCES kturV2.Genre(id_genre)
);

CREATE TABLE kturV2.User_Author (
    id_lecteur INT,
    id_author INT,
    PRIMARY KEY (id_lecteur, id_author),
    FOREIGN KEY (id_lecteur) REFERENCES kturV2.User(id_lecteur),
    FOREIGN KEY (id_author) REFERENCES kturV2.Author(author_id)
);

CREATE OR REPLACE FUNCTION prevent_duplicate_genre()
RETURNS TRIGGER AS $$
BEGIN
    -- Vérifier si le genre existe déjà (indépendamment de la casse)
    IF EXISTS (SELECT 1 FROM kturV2.Genre WHERE LOWER(genre_name) = LOWER(NEW.genre_name)) THEN
        -- Si le genre existe déjà, ignorer l'insertion
        RETURN NULL;  -- Empêche l'insertion du doublon
    END IF;

    -- Si aucun doublon n'est trouvé, autoriser l'insertion
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER genre_no_duplicates
BEFORE INSERT ON kturV2.Genre
FOR EACH ROW
EXECUTE FUNCTION prevent_duplicate_genre();

CREATE TEMPORARY TABLE temp_genre_votes (
    id_book INTEGER,
    genre_name VARCHAR(255),
    nb_vote INTEGER
);


CREATE VIEW view_genre_votes AS
SELECT
    t.id_book,
    g.id_genre,
    t.nb_vote
FROM
    temp_genre_votes t
JOIN
    kturV2.Genre g ON t.genre_name = g.genre_name;
         
WbImport -file=/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/transformed_genre_votes.csv
         -type=text
         -header=true
         -table= temp_genre_votes
         -delimiter= ','

INSERT INTO kturV2.Vote (id_book, id_genre, nb_vote)
SELECT id_book, id_genre, nb_vote
FROM view_genre_votes;

SELECT * FROM view_genre_votes;

----------------
-- Peuplement --
----------------


--Peuplement de la table Publisher
WbImport
  -file=/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/unique_publishers.csv
  -type=text
  -table=kturV2.Publisher
  -header=true
  -delimiter=','
  
--Peuplement de la table Serie
WbImport
  -file=/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/unique_series.csv
  -type=text
  -table=kturV2.Serie
  -header=true
  -delimiter=','
  
--Peuplement de la table Book
WbImport
  -file=/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/liste_books.csv
  -type=text
  -table=kturV2.Book
  -header=true
  -delimiter=','
  -multiline=true
  -continueOnError=true

--Peuplement de la table Genre
WbImport -file=/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/unique_genres.csv
         -type=text
         -header=true
         -table= kturV2.Genre
         -delimiter= ','
         -importColumns=genre_name

--Peuplement de la table Author
WbImport
  -file=/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/liste_authors.csv
  -type=text
  -table=kturV2.Author
  -header=true
  -delimiter=','
  -continueOnError=true
  
--Peuplement de la table Characters
WbImport
  -file=/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/unique_characters.csv
  -type=text
  -table=kturV2.Character
  -header=true
  -delimiter=','
  -continueOnError=true
  
--Peuplement de la table Settings
WbImport
  -file=/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/csv_propre/unique_settings.csv
  -type=text
  -table=kturV2.Setting
  -header=true
  -delimiter=','
  -continueOnError=true
  
--Peuplement de la table Author
WbImport
  -file=/home/etuinfo/dmeur/Documents/SAE/Reco_Ktur/bdd/genre_author.csv
  -type=text
  -table=kturV2.Genre_Author
  -header=true
  -delimiter=','
