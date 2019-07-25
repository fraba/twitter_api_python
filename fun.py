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
        cursor.execute("INSERT OR IGNORE INTO tweet (id, coordinates, created_at, current_user_retweet, favorite_count, favorited, in_reply_to_status_id, in_reply_to_user_id, place, retweet_count, retweeted_status_id, source, text, user_id, lang) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (tweet['id'], tweet['coordinates'], tweet['created_at'], tweet['current_user_retweet'], tweet['favorite_count'], tweet['favorited'], tweet['in_reply_to_status_id'], tweet['in_reply_to_user_id'], tweet['place'], tweet['retweet_count'], tweet['retweeted_status_id'], tweet['source'], tweet['text'], tweet['user_id'], tweet['lang']))
        conn.commit()
    except sqlite3.Error as e:
        print "Database error entering tweets:", e.args[0]
        pass

    return

def enterHashtag(tweet_id, hashtag, db):

    try: 
        conn = sqlite3.connect(db, timeout=10)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO hashtag (tweet_id, text) VALUES (?, ?)", (tweet_id, hashtag['text']))
        conn.commit()
    except sqlite3.Error as e:
        print "Database error entering hashtag:", e.args[0]
        pass

    return

def enterMedia(tweet_id, media, db):

    try: 
        conn = sqlite3.connect(db, timeout=10)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO media (tweet_id, media_id, type, media_url, expanded_url) VALUES (?, ?, ?, ?, ?)", (tweet_id, media['id_str'],  media['type'],  media['media_url'],  media['expanded_url']))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error entering media:", e.args[0])
        pass

    return

def enterUrl(tweet_id, url, db):

    try: 
        conn = sqlite3.connect(db, timeout=10)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO url (tweet_id, expanded_url) VALUES (?, ?)", (tweet_id, url['expanded_url']))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error entering url:", e.args[0])
        pass

    return

def enterUserMention(tweet_id, user_mention, db):

    try: 
        conn = sqlite3.connect(db, timeout=10)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO user_mention (tweet_id, name, screen_name, user_id) VALUES (?, ?, ?, ?)", (tweet_id, user_mention['name'], user_mention['screen_name'], user_mention['id_str'],))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error entering user_mention:", e.args[0])
        pass

    return

    

def parseTweet(tweet_source, DB):

    # It takes a dictionary of a single tweet and return a dictionary of a single tweet!
    
    tweet = {}

    tweet['id'] = tweet_source.get('id_str').encode('utf-8')
    if tweet_source['coordinates']:
        tweet['coordinates'] = json.dumps(tweet_source['coordinates'])
    else:    
        tweet['coordinates'] = ''
    if tweet_source['lang']:
        tweet['lang'] = json.dumps(tweet_source['lang'])
    else:    
        tweet['lang'] = ''
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
    tweet['source'] = tweet_source.get('source', '').encode('utf-8')

    if 'retweeted_status' in tweet_source:
        # TWEET IS a RETWEET
        parseTweet(tweet_source['retweeted_status'], DB)
        print('>>>> Retweet <<<<')
        tweet['retweeted_status_id'] = tweet_source['retweeted_status'].get('id_str','').encode('utf-8')
        
        if 'hashtags' in tweet_source['retweeted_status']['entities']:
            for hashtag in tweet_source['retweeted_status']['entities']['hashtags']:
                enterHashtag(tweet['retweeted_status_id'], hashtag, DB)
        if 'media' in tweet_source['retweeted_status']['entities']:
            for medium in tweet_source['retweeted_status']['entities']['media']:
                enterMedia(tweet['retweeted_status_id'], medium, DB)
        if 'urls' in tweet_source['retweeted_status']['entities']:
            for url in tweet_source['retweeted_status']['entities']['urls']:
                enterUrl(tweet['retweeted_status_id'], url, DB)
        if 'user_mentions' in tweet_source['retweeted_status']['entities']:
            for user_mention in tweet_source['retweeted_status']['entities']['user_mentions']:
                enterUserMention(tweet['retweeted_status_id'], user_mention, DB)
            
        if 'extended_tweet' in tweet_source['retweeted_status']:
            tweet['text'] = tweet_source['retweeted_status']['extended_tweet'].get('full_text', '').encode('utf-8')
            print('>>>> Exenteded Tweet <<<<')
        else:     
            tweet['text'] = tweet_source['retweeted_status'].get('text', '').encode('utf-8')
    else:
        # TWEET IS NOT a RETWEET
        tweet['retweeted_status_id'] = ''

        if 'hashtags' in tweet_source['entities']:
            for hashtag in tweet_source['entities']['hashtags']:
                enterHashtag(tweet['id'], hashtag, DB)
        if 'media' in tweet_source['entities']:
            for medium in tweet_source['entities']['media']:
                enterMedia(tweet['id'], medium, DB)
        if 'urls' in tweet_source['entities']:
            for url in tweet_source['entities']['urls']:
                enterUrl(tweet['id'], url, DB)
        if 'user_mentions' in tweet_source['entities']:
            for user_mention in tweet_source['entities']['user_mentions']:
                enterUserMention(tweet['id'], user_mention, DB)
        
        if 'extended_tweet' in tweet_source:
           tweet['text'] = tweet_source['extended_tweet'].get('full_text', '').encode('utf-8')
           print('>>>> Exenteded Tweet <<<<')
        else:     
            tweet['text'] = tweet_source.get('text', '').encode('utf-8')
    tweet['user_id'] = tweet_source['user'].get('id_str').encode('utf-8')

    enterTweet(tweet, DB)

    return

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
    if tweet_source['user']['location']:
        user['location'] = tweet_source['user'].get('location','').encode('utf-8')
    else:
        user['location'] = ''
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
    # user['withheld_in_countries'] = tweet_source['user'].get('withheld_in_countries','').encode('utf-8')
    user['withheld_in_countries'] = ''
    
    return user    
    
def manageApiResponse(search_or_error_string, error_bool, db):
    try:
        conn = sqlite3.connect(db, timeout=10)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("INSERT INTO log (status, error) VALUES (?, ?)", (str(search_or_error_string), str(error_bool)))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error entering log:", e.args[0])

    return
