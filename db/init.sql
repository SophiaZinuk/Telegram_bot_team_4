-- Before execution create DB with name "residental_bot". Make sure user is "postgres" and password is "postgres

CREATE TABLE IF NOT EXISTS users
(
    id           serial PRIMARY KEY,
    address      VARCHAR(50) NOT NULL,
    user_type    VARCHAR(50) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    chat_id      INT
);

CREATE TABLE IF NOT EXISTS applications
(
    id               serial PRIMARY KEY,
    created_by       INT         NOT NULL,
    application_type VARCHAR(50) NOT NULL,
    description      VARCHAR(200),
    created_at       TIMESTAMP DEFAULT current_timestamp,
    CONSTRAINT fk_user FOREIGN KEY (created_by) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS application_data
(
    id             serial PRIMARY KEY,
    car_number     VARCHAR(50),
    application_id INT NOT NULL,
    CONSTRAINT fk_application FOREIGN KEY (application_id) REFERENCES applications (id)
);


INSERT INTO users (address, user_type, phone_number)
VALUES ('Шевченка 23. кв 33',
        'USER',
        '+380914543783');


INSERT INTO users (address, user_type, phone_number)
VALUES ('Бандери 2. кв 12',
        'USER',
        '+3806345343322');
