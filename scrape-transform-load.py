""""
Author: Alex ONeill
Author: Gio Abou Jaoude
Author: Noah Ponticiello

Group Project: Visualizing Near Real-Time Reddit r/wallstreetbets Chatter Volume Alongside Trading Volume
https://github.com/alex-oneill/Visualizing-Reddit-Chatter-Stock-Movement

CS666 - Enterprise Intelligence Development (Pace University)
Spring 2021 - Prof. Barabasi
"""

import psycopg2
from configparser import ConfigParser
import requests
from bs4 import BeautifulSoup as bs
import time
import praw
from praw import Reddit
from collections import namedtuple


# SECTION: MAKE REDDIT OBJ
def make_reddit() -> Reddit:
    """Creates PRAW Reddit OBJ with masked creds from the praw.ini file.
        Format as:
            [reddit]
            client_id=myclientid
            client_secret=mysecretcode
            user_agent=applicationname
            username=personalusername
            password=personalpassword
    """
    reddit = praw.Reddit('reddit')
    return reddit


# SECTION: SCRAPE
# TODO: SCRAPE REDDIT
def scrape_reddit(red_instance: Reddit):
    """Scrapes subreddit r/wallstreetbets for the most recent posts and comments."""
    subreddit = red_instance.subreddit('wallstreetbets')
    Comment = namedtuple('Comment', ['comment_id', 'comment_time', 'comment_text', 'submission_id',
                                     'submission_title', 'submission_text'])

    for comment in subreddit.stream.comments(skip_existing=True):
        sub_id, sub_title, sub_text = comment.submission.id, comment.submission.title, comment.submission.selftext
        com_id, com_timestamp, com_text = comment.id, comment.created_utc, comment.body

        com_tup = Comment(com_id, com_timestamp, com_text, sub_id, sub_title, sub_text)

        # TODO: SAVE COMMENT TO DB?

        # NOTE: INSTEAD OF SAVING EACH ROW, PARSE AND SAVE SCORES
        points = parse_reddit(com_tup)
        store_points_list(points)
        # print(red_instance.auth.limits) # NOTE: REMAINING API CALLS/SESSION


# TODO: SCRAPE TICKER INFO
def scrape_ticker_info():
    """The function will scrape the ticker symbol, current price, and trading volume and return a raw text result."""


# SECTION: PARSING & EXTRACTING
# TODO: PARSE TICKER INFO
def parse_ticker():
    """Takes in raw ticker info from ticker scraping, parses out text, and returns symbol data."""


def parse_reddit(comment: tuple) -> tuple:
    """Tags posts and comments based on the ticker that is being discussed."""
    patterns = ['gme', 'gamestop', 'game stop']

    # NOTE: ALL ROWS TO LOWER() FOR MATCHING
    clean_com = ' '.join(word.lower() for word in comment.comment_text.split())
    clean_sub_title = ' '.join(word.lower() for word in comment.submission_title.split())
    clean_sub_text = ' '.join(word.lower() for word in comment.submission_text.split())

    # NOTE: SCORE BASED ON MATCH TYPE (COMMENT, TOPIC TITLE, TOPIC TEXT)
    if any(match in clean_com for match in patterns):
        # print(f'1 pt -- MATCH (comment): {clean_com}\n\tSUB: {clean_sub_title}')
        com_point = 1
    elif any(match in clean_sub_title for match in patterns):
        # print(f'.5 pt -- MATCH (sub-title): {clean_sub_title}\n\tCOMMENT: {clean_com}')
        com_point = 0.5
    elif any(match in clean_sub_text for match in patterns):
        # print(f'.5 pt -- MATCH (sub-text): {clean_sub_text}\n\tCOMMENT: {clean_com}')
        com_point = 0.5
    else:
        # print(f'0 pt -- NOT-MATCH: {clean_com}\n\tSUB: {clean_sub_title}')
        com_point = 0

    # NOTE: DUMP COMMENT TEXT AND LEAVE ID FEATURES + SCORES
    Points = namedtuple('Points', ['comment_time', 'comment_id', 'points'])
    point_tup = Points(comment.comment_time, comment.comment_id, com_point)
    return point_tup


# SECTION: LOAD TO DB
def store_points_list(point_tup: tuple) -> None:
    # FIXME: HOW DO MAKE A BULK LOAD LIST???

# TODO: LOAD REDDIT TO POSTGRESQL
def load_reddit():
    """Loads cleaned and formatted reddit content to the reddit database table."""
    # NOTE: define variables
    # cur.execute("""INSERT INTO <table> (<col1, col2, col3...>)
    #             VALUES (%s, %s, %s, %s)""",
    #             (<var1, var2, var3...>))
    # conn.commit()


# TODO: LOAD TICKER TO POSTGRESQL
def load_ticker():
    """Loads cleaned and formatted ticker content to the ticker database table."""
    # NOTE: define variables
    # cur.execute("""INSERT INTO <table> (<col1, col2, col3...>)
    #             VALUES (%s, %s, %s, %s)""",
    #             (<var1, var2, var3...>))
    # conn.commit()


# SECTION: MAIN()
def main():
    """Main run logic when initiated via command line."""
    # TODO: MAIN LOGIC
    """"
        > while market_hours:
            > scrape reddit
                -> scrape ticker info
            > parse and clean html from reddit and ticker requests
            > extract ticker info and other data from reddit posts
            > load formatted reddit and ticker info to postgres
            > wait X minutes... then continue
    """
    reddit = make_reddit()
    scrape_reddit(reddit)


if __name__ == '__main__':
    main()
