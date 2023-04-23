CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    pword TEXT,
    system_role TEXT
);

CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    skill_level TEXT,
    price INTEGER,
    max_riders INTEGER,
    lesson_date DATE, 
    lesson_time TIME
);

CREATE TABLE horses (
    id SERIAL PRIMARY KEY,
    horse_name TEXT,
    birthyear INTEGER,
    max_lessons INTEGER,
    feed TEXT,
    feed_amount INTEGER,
    visible BOOLEAN
);

CREATE TABLE riders (
    id  SERIAL PRIMARY KEY,
    rider_name TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE lesson_riders (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons,
    rider_id INTEGER REFERENCES riders,
    horse_id INTEGER REFERENCES horses
);