-- Steam ETL Database Schema (SQLite version)
-- This schema is to define all the tables and relationships for my capstone project.

-- Drop existing tables (for dev reset purposes)

DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS descriptions;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS promotional;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS steam_spy;
DROP TABLE IF EXISTS tags;

-- Core table: games
-- Stores main game information

CREATE TABLE games (
    appid INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    release_date TEXT,
    is_free BOOLEAN, -- This boolean is technically unnecessary.
    -- last_updated_price TEXT, -- This is redundant with the 'steamspy' table
    -- languages TEXT, -- This is redundant with the 'steamspy' table
    release_type TEXT -- This is to define weather the games are a 'demo' or 'game'. 
);

-- Categories table
-- Stores game categories
CREATE TABLE categories (
    appid INTEGER,
    category TEXT,
    FOREIGN KEY (appid) REFERENCES games(appid)
);

-- Descriptions table
-- Stores game descriptions

CREATE TABLE descriptions (
    appid INTEGER,
    game_summary TEXT,
    FOREIGN KEY (appid) REFERENCES games(appid)
);

-- Genres table
-- Stores game genres
-- This table is not necessary, it may be useful for some nul data with the steamspy table.
CREATE TABLE genres (
    appid INTEGER,
    genre TEXT,
    FOREIGN KEY (appid) REFERENCES games(appid)
);

-- Promotional table
-- Stores promotional media links, 
-- Not all games have promotional media.

CREATE TABLE promotional (
    appid INTEGER,
    Head_image TEXT,
    background_image TEXT,
    screenshot_1 TEXT,
    trailer TEXT,
    FOREIGN KEY (appid) REFERENCES games(appid)
);

-- Reviews table
-- Stores user reviews and scores

CREATE TABLE reviews (
    appid INTEGER,
    review_score INTEGER, -- out of 10
    review_score_text TEXT,
    positive_likes INTEGER,
    negative_dislikes INTEGER,
    total_reviews INTEGER,
    recommendations INTEGER,
    FOREIGN KEY (appid) REFERENCES games(appid)
);

-- Steamspy table
-- Stores additional game data from Steamspy
-- This table is clear and concise,
-- and is superior to the genres table.
CREATE TABLE steam_spy (
    appid INTEGER,
    developer TEXT,
    publisher TEXT,
    price INTEGER, -- superior to the games table
    languages INTEGER, -- superior to the games table
    genre TEXT, -- superior to genres table
    FOREIGN KEY (appid) REFERENCES games(appid)
);

-- tags table
-- Stores game tags

CREATE TABLE tags (
    appid INTEGER,
    tag TEXT,
    FOREIGN KEY (appid) REFERENCES games(appid)
);