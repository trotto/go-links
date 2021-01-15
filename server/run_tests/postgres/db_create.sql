DROP DATABASE IF EXISTS testing_trotto_core;
DROP USER IF EXISTS admin;

CREATE USER admin WITH PASSWORD 'testing';

CREATE DATABASE testing_trotto_core;

GRANT ALL PRIVILEGES ON DATABASE "testing_trotto_core" to admin;
