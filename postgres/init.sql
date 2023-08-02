CREATE DATABASE bbdd_posts;

\c bbdd_posts;

CREATE TABLE posts (id SERIAL PRIMARY KEY,
					titulo VARCHAR(20),
					contenido VARCHAR(50),
					fecha DATE);
