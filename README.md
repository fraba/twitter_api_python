# Twitter API with Python

Simple scripts to query the Twitter API and store the results in a SQLite database. It uses the `TwitterAPI` module (see [github.com/geduldig/TwitterAPI](https://github.com/geduldig/TwitterAPI)).

## Prerequisites

You will need to install the following Python modules: `sqlite3`, `json` and `TwitterAPI`.

## Getting started

1. You  need to download all the `.py` files.
2. Edit the `local_info.py` file to include your API credentials.
3. Create a database with `python createdb.py [database name]` (replace [database name] with your actual database name, omit `.sqlite` - it will be added automatically).
4a. If you want to search Twitter based on selected keywords, edit the `search_list`  in `search_twitter.py` and launch the script with `python search_twitter.py [database name]` (omit `.sqlite`).
4b If you want to parse all the available tweets from a specific user, edit the `twitter_screen_name` in `get_user_timeline.py` and launch the script with `python get_user_timeline.py [database name]` (omit `.sqlite`).
