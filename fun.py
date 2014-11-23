#!/usr/bin/env python

# fun.py

import sqlite3
import json

def enterUser(user, db):

    # It takes a dictionary of a single tweet!

    try:
        conn = sqlite3.connect(db, timeout=10)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO user (id, name, screen_name, created_at, default_profile, default_profile_image, description, favourites_count, followers_count, friends_count, listed_count, location, lang, statuses_count, time_zone, url, verified, withheld_in_countries) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user['id'], user['name'], user['screen_name'], user['created_at'], user['default_profile'], user['default_profile_image'], user['description'], user['favourites_count'], user['followers_count'], user['friends_count'], user['listed_count'], user['location'], user['lang'], user['statuses_count'], user['time_zone'], user['url'], user['verified'], user['withheld_in_countries']))
        conn.commit()
    except sqlite3.Error as e:
        print "Database error entering users:", e.args[0]
        pass

    return

def enterTweet(tweet, db):

    # It takes a dictionary of a single tweet!

    try: 
        conn = sqlite3.connect(db, timeout=10)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO tweet (id, coordinates, created_at, current_user_retweet, favorite_count, favorited, in_reply_to_status_id, in_reply_to_user_id, place, retweet_count, retweeted_status_id, source, text, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (tweet['id'], tweet['coordinates'], tweet['created_at'], tweet['current_user_retweet'], tweet['favorite_count'], tweet['favorited'], tweet['in_reply_to_status_id'], tweet['in_reply_to_user_id'], tweet['place'], tweet['retweet_count'], tweet['retweeted_status_id'], tweet['source'], tweet['text'], tweet['user_id']))
        conn.commit()
    except sqlite3.Error as e:
        print "Database error entering tweets:", e.args[0]
        pass

    return

def parseTweet(tweet_source):

    # It takes a dictionary of a single tweet and return a dictionary of a single tweet!
    
    tweet = {}

    tweet['id'] = tweet_source.get('id_str').encode('utf-8')
    if tweet_source['coordinates']:
        tweet['coordinates'] = json.dumps(tweet_source['coordinates'])
    else:    
        tweet['coordinates'] = ''
    tweet['created_at'] = tweet_source.get('created_at').encode('utf-8')
    if 'current_user_retweet' in tweet_source:
        tweet['current_user_retweet'] = tweet_source['current_user_retweet'].get('id_str').encode('utf-8')
    else:
         tweet['current_user_retweet'] = ''
    tweet['favorite_count'] = tweet_source.get('favorite_count','')
    tweet['favorited'] = tweet_source.get('favorited','')
    tweet['in_reply_to_status_id'] = tweet_source.get('in_reply_to_status_id_str','')
    tweet['in_reply_to_user_id'] = tweet_source.get('in_reply_to_user_id_str','')
    if tweet_source['place']:
        tweet['place'] = json.dumps(tweet_source['place'])
    else:
        tweet['place'] = ''
    tweet['retweet_count'] = tweet_source.get('retweet_count', '')
    if 'retweeted_status' in tweet_source:
        tweet['retweeted_status_id'] = tweet_source['retweeted_status'].get('id_str','').encode('utf-8')
    else:
        tweet['retweeted_status_id'] = ''
    tweet['source'] = tweet_source.get('source', '').encode('utf-8')
    tweet['text'] = tweet_source.get('text', '').encode('utf-8')
    tweet['user_id'] = tweet_source['user'].get('id_str').encode('utf-8')

    return tweet

def parseUser(tweet_source):

    # It takes a dictionary of a single tweet and return a dictionary of a single tweet!
    
    user = {}

    user['id'] = tweet_source['user'].get('id_str').encode('utf-8')
    user['name'] = tweet_source['user'].get('name','').encode('utf-8')
    user['screen_name'] = tweet_source['user'].get('screen_name','').encode('utf-8')
    user['created_at'] = tweet_source['user'].get('created_at','').encode('utf-8')
    user['default_profile'] = tweet_source['user'].get('default_profile','')
    user['default_profile_image'] = tweet_source['user'].get('default_profile_image','')
    user['description'] = tweet_source['user'].get('description','')
    user['favourites_count'] = tweet_source['user'].get('favourites_count','')
    user['followers_count'] = tweet_source['user'].get('followers_count','')
    user['friends_count'] = tweet_source['user'].get('friends_count','')
    user['listed_count'] = tweet_source['user'].get('listed_count','')
    user['location'] = tweet_source['user'].get('location','').encode('utf-8')
    user['lang'] = tweet_source['user'].get('lang','').encode('utf-8')
    user['statuses_count'] = tweet_source['user'].get('statuses_count','')
    if tweet_source['user']['time_zone']:
        user['time_zone'] = tweet_source['user'].get('time_zone','').encode('utf-8')
    else:
        user['time_zone'] = ''
    if tweet_source['user']['url']:
        user['url'] = tweet_source['user'].get('url','').encode('utf-8')
    else:
        user['url'] = ''
    user['verified'] = tweet_source['user'].get('verified','')
    user['withheld_in_countries'] = tweet_source['user'].get('withheld_in_countries','').encode('utf-8')
    
    return user    
    
def manageApiResponse(search_or_error_string, error_bool, db):
    try:
        conn = sqlite3.connect(db, timeout=10)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("INSERT INTO log (status, error) VALUES (?, ?)", (str(search_or_error_string), str(error_bool)))
        conn.commit()
    except sqlite3.Error as e:
        print "Database error entering log:", e.args[0]

    return
