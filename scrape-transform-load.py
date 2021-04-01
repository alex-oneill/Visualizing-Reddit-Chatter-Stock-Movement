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


# SECTION: SCRAPE
# TODO: SCRAPE REDDIT
def scrape_reddit():
    """Scrapes subreddit r/wallstreetbets for the most recent posts and comments."""
    # NOTE: SCRAPE REDDIT POSTS AND COMMENTS FROM r/wallstreetbets


# TODO: SCRAPE TICKER INFO
def scrape_ticker_info():
    """The function will scrape the ticker symbol, current price, and trading volume and return a raw text result."""


# SECTION: PARSING
# TODO: PARSE REDDIT
def parse_reddit():
    """Takes in raw data from reddit scraping, parses out text, and returns wanted data."""


# TODO: PARSE TICKER INFO
def parse_ticker():
    """Takes in raw ticker info from ticker scraping, parses out text, and returns symbol data."""


# SECTION: TRANSFORMING AND EXTRACTING TICKER
# TODO: EXTRACT TICKER FROM REDDIT
def extract_ticker():
    """Tags posts and comments based on the ticker that is being discussed."""


# SECTION: LOAD TO DB
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


if __name__ == '__main__':
    main()
