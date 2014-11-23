#!/usr/bin/env python

# stream_twitter.py

search_list = ['wordone', 'wordtwo', 'wordthree'] # let's define all words we would like to have a look for

import sys, os, inspect, json
import random
from time import sleep

# Receive the argument from bash or return error message
call_error_msg = "Error: This script requires at least one argument: the database filename."
try:
    DB = sys.argv[1] + '.sqlite'
except IndexError:
    sys.exit(call_error_msg)

# To search additional modules in the same directory
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from fun import *        
from local_info import *
from TwitterAPI import TwitterAPI

api = TwitterAPI(twitter_auth_dict['consumer_key'], twitter_auth_dict['consumer_secret'], twitter_auth_dict['access_token'], twitter_auth_dict['access_token_secret'])


while True:
#    try:

    q = ",".join(random.sample(search_list,3))

    # q = "pizza"

    print q

    r = api.request('statuses/filter', {'track':q})
    # r = api.request('statuses/filter', {'locations':'-122.75,36.8,-121.75,37.8'})
    # r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
    # print r.get_iterator()
    for item in r.get_iterator():
    ## print item
        print( '@%s tweeted: %s' % ( item['user']['screen_name'], item['text'] ) )
        tweet = parseTweet(item)
        enterTweet(tweet, DB)
        user = parseUser(item)
        enterUser(user, DB)
#    except:
#        pass

    print 'Sleeping a while test...'    
    sleep(5)    
