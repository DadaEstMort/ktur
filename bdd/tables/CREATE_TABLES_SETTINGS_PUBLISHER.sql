DROP schema if exists saebdd cascade;
create schema saebdd;
set schema 'saebdd';

CREATE TABLE Publisher (
  id_publisher INTEGER PRIMARY KEY,
  name VARCHAR,
  id_book INTEGER
);

create table Book(
  id_book integer primary key,
  title varchar,
  nmber_of_page integer,
  date_published date,
  original_title varchar,
  isbn integer,
  isbn13 integer,
  description varchar,
  id_publisher INTEGER,
  FOREIGN KEY (id_publisher) REFERENCES Publisher(id_publisher)
  );

CREATE TABLE Setting (
  id_setting INTEGER PRIMARY KEY,
  setting_name VARCHAR,
  id_book INTEGER
);

CREATE TABLE BookSetting (
  id_book INTEGER,
  id_setting INTEGER,
  PRIMARY KEY (id_book, id_setting),
  FOREIGN KEY (id_book) REFERENCES Book(id_book),
  FOREIGN KEY (id_setting) REFERENCES Setting(id_setting)
);

WbImport
-file='/home/etuinfo/gleonplevert/Documents/S5/SAE/Settings.csv'
-type=text
-table=Setting
-header=true
  
