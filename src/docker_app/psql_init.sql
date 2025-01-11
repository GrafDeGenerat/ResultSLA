CREATE DATABASE demo_sql_sla;

\c demo_sql_sla

CREATE TABLE users_table (
    id SERIAL NOT NULL PRIMARY KEY,
    username VARCHAR(30) UNIQUE,
    password VARCHAR(30)
);

INSERT INTO users_table (username, password)
VALUES (
        'Bob',
        123
);