#!/usr/bin/env python

# createdb.py

# Call it from console passing database filename: python createdb.py filename

import sqlite3
import sys

# Receive the argument from bash
filename = sys.argv[1] + '.sqlite'

# Receive the argument from bash
filename = sys.argv[1] + '.sqlite'
 
conn = sqlite3.connect(filename)
 
cursor = conn.cursor()
 
# Create database

# Create tables
cursor.execute("""
-- Table: user
CREATE TABLE user ( 
    id                    CHAR PRIMARY KEY,
    name                  CHAR,
    screen_name           CHAR,
    created_at            DATETIME,
    default_profile       BOOLEAN,
    default_profile_image BOOLEAN,
    description           TEXT,
    favourites_count      INTEGER,
    followers_count       INTEGER,
    friends_count         INTEGER,
    listed_count          INTEGER,
    lang                  CHAR,
    location              TEXT,
    statuses_count        INTEGER,
    time_zone             TEXT,
    url                   CHAR,
    verified              BOOLEAN,
    withheld_in_countries CHAR,
    timestamp             DATETIME DEFAULT ( CURRENT_TIMESTAMP ) 
    );
               """)

cursor.execute("""
-- Table: tweet
CREATE TABLE tweet (
    id CHAR PRIMARY KEY,
    coordinates TEXT,
    created_at DATETIME,
    current_user_retweet INTEGER,
    favorite_count INTEGER,
    favorited BOOLEAN,
    in_reply_to_status_id CHAR,
    in_reply_to_user_id CHAR,
    place TEXT,
    lang TEXT,
    retweet_count INTEGER,
    retweeted_status_id CHAR,
    source CHAR,
    text TEXT,
    hashtags TEXT,
    media TEXT,
    urls TEXT,
    user_mentions TEXT,
    user_id CHAR REFERENCES user ( id ),
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ) 
    );
               """)

cursor.execute("""
-- Table: hashtag
CREATE TABLE hashtag (
    tweet_id CHAR,
    text CHAR,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ),
    PRIMARY KEY (tweet_id, text)
    );
               """)

cursor.execute("""
-- Table: media
CREATE TABLE media (
    tweet_id CHAR,
    media_id CHAR,
    type CHAR,
    media_url CHAR,
    expanded_url CHAR, 
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ),
    PRIMARY KEY (tweet_id, media_id)
    );
               """)

cursor.execute("""
-- Table: url
CREATE TABLE url (
    tweet_id CHAR,
    expanded_url CHAR,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ),
    PRIMARY KEY (tweet_id, expanded_url)
    );
               """)

cursor.execute("""
-- Table: user_mention
CREATE TABLE user_mention (
    tweet_id CHAR,
    name CHAR, 
    screen_name CHAR, 
    user_id CHAR,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ),
    PRIMARY KEY (tweet_id, user_id)
    );
               """)



cursor.execute("""
-- Table: log
CREATE TABLE log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status CHAR,
    error CHAR,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ) 
    );
               """)


# Close connection
conn.commit()
