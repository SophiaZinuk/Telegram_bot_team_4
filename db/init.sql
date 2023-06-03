CREATE DATABASE residental_bot;

CREATE TABLE IF NOT EXISTS users (
                          id serial PRIMARY KEY,
                          address VARCHAR ( 50 ) NOT NULL,
                          user_type VARCHAR ( 50 ) NOT NULL,
                          phone_number VARCHAR (50) NOT NULL,
                          chat_id INT
);
INSERT INTO users (address, user_type, phone_number) VALUES ('Шевченка 23. кв 33', 'USER', '+380914543783');
INSERT INTO users (address, user_type, phone_number) VALUES ('Бандери 2. кв 12', 'USER', '+3806345343322')
