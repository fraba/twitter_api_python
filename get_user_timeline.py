#!/usr/bin/env python

# get_user_timeline.py

twitter_screen_name = '' # e.g. katyperry, justinbieber, BarackObama

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
from TwitterAPI import TwitterPager

api = TwitterAPI(twitter_auth_dict['consumer_key'], twitter_auth_dict['consumer_secret'], twitter_auth_dict['access_token'], twitter_auth_dict['access_token_secret'])

try:
    r = TwitterPager(api, 'statuses/user_timeline',
                         {'screen_name':twitter_screen_name,
                              'count':'500', 'include_rts':'false',
                         'exclude_replies':'false'})
    
    for item in r.get_iterator():
        ## print item
        print( '@%s tweeted: %s' % ( item['user']['screen_name'], item['text'] ) )
        parseTweet(item, DB)
        user = parseUser(item)
        enterUser(user, DB)
except Exception as e:
    print 'Crushed with error\n' + str(e)
    print 'Sleeping a bit...'
    sleep(60)
    pass  
