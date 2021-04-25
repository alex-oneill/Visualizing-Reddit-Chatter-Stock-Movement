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
import praw
import requests
from praw import Reddit
from collections import namedtuple
from ChartVal import ChartVal


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
    red_instance = praw.Reddit('reddit')
    return red_instance


# SECTION: SCRAPE
def scrape_reddit(red_instance: Reddit):
    """Scrapes subreddit r/wallstreetbets for the most recent posts and comments."""
    subreddit = red_instance.subreddit('wallstreetbets')
    Comment = namedtuple('Comment', ['comment_id', 'comment_time', 'comment_text', 'submission_id',
                                     'submission_title', 'submission_text'])

    start_time, com_counter = 0, 0
    points_store = {'start_time': 0, 'comment_count': 0, 'group_points': 0}
    for comment in subreddit.stream.comments(skip_existing=True):
        sub_id, sub_title, sub_text = comment.submission.id, comment.submission.title, comment.submission.selftext
        com_id, com_timestamp, com_text = comment.id, int(comment.created_utc), comment.body

        # NOTE: INITIATED COUNTERS AT FIRST COMMENT
        if com_counter == 0:
            start_time = com_timestamp
            points_store['start_time'] = start_time
            print('Clean Start: ', start_time)
            print('INIT::', points_store, '\n')

        com_tup = Comment(com_id, com_timestamp, com_text, sub_id, sub_title, sub_text)

        # NOTE: INSTEAD OF SAVING EACH ROW, PARSE AND SAVE SCORES
        points = parse_reddit(com_tup)
        # print(points)
        com_counter += 1

        # NOTE: RESET COUNTER IF 60 SEC HAS ELAPSED SINCE FIRST COMMENT IN GROUPING
        if points.comment_time - start_time > 60:
            print('CLOSED STORE:', points_store)
            store_points_list(points_store)
            chart_data.add_points(points_store)  # NOTE: STORE POINT DATA IN CLASS
            scrape_ticker_info(start_time)  # NOTE: GRAB TICKER INFO
            # print(chart_data)
            print('\n', red_instance.auth.limits, '\n')  # NOTE: REMAINING API CALLS/SESSION
            print('Restart INIT:', points)
            start_time, com_counter = points.comment_time, 1
            points_store['start_time'] = start_time
            points_store['comment_count'] = com_counter
            points_store['group_points'] = points.points
            print(points_store)
        # NOTE: APPEND COUNTERS IF WITHIN 60 SEC OF FIRST COMMENT PER GROUPING
        else:
            points_store['comment_count'] = com_counter
            points_store['group_points'] += points.points
            # print(points_store)
            # print('\n', red_instance.auth.limits, '\n')  # NOTE: REMAINING API CALLS/SESSION


def iex_config(filename='./iex.ini') -> str:
    """Reads and returns IEX API token from config file.
        Format as:
            [iex]
            sbox_token=sandboxtoken
            token=productioncloudtoken
    """
    parser = ConfigParser()
    parser.read(filename)
    section = parser['iex']
    token = section['token']
    return token


def scrape_ticker_info(start: int) -> None:
    """The function grabs the current price and trading volume via IEX API. Returns these values and section scrape
    time that is being used as a PK for reddit scraping."""
    TickerValues = namedtuple('TickerValues', ['start_time', 'end_price', 'end_volume'])
    token = iex_config()
    ticker = 'GME'
    base_url = f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={token}'
    stock_data = requests.get(base_url).json()

    ticker_tup = TickerValues(start, stock_data['iexRealtimePrice'], stock_data['iexVolume'])  # NOTE: MKT HOURS
    # ticker_tup = TickerValues(start, stock_data['latestPrice'], stock_data['latestVolume'])  # NOTE: OFF HOURS
    load_ticker(ticker_tup)
    chart_data.add_stock(ticker_tup)
    chart_data.write_csv()
    print(ticker_tup)


# SECTION: PARSING & EXTRACTING
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
def db_config(filename='./database.ini', section='postgres'):
    """Establishes connection to local postgres db with masked credentials.
        Format as:
                [postgres]
                host=localhost
                database=databasename
                user=mypostgresusername
                password=mypostgrespassword
    """
    parser = ConfigParser()
    parser.read(filename)
    db_conn = {}
    for param in parser.items(section):
        db_conn[param[0]] = param[1]
    return db_conn


def store_points_list(point_store: dict) -> None:  # NOTE: STORING REDDIT POINT VALUES
    """Creates reddit points table and stores comment points each minute to the DB"""
    mk_table = """CREATE TABLE IF NOT EXISTS reddit_points (
                group_timestamp integer not null,
                comment_count  integer not null,
                group_points float(1) not null);"""
    cur.execute(mk_table)
    conn.commit()
    cur.execute("""INSERT INTO reddit_points (group_timestamp, comment_count, group_points)
                VALUES (%s, %s, %s)""",
                (point_store['start_time'], point_store['comment_count'], point_store['group_points']))
    conn.commit()


# TODO: LOAD FULL REDDIT COMMENTS TO POSTGRESQL
def load_reddit():
    """Loads cleaned and formatted reddit content to the reddit database table."""
    # NOTE: define variables
    # cur.execute("""INSERT INTO <table> (<col1, col2, col3...>)
    #             VALUES (%s, %s, %s, %s)""",
    #             (<var1, var2, var3...>))
    # conn.commit()


def load_ticker(ticker_info: tuple) -> None:  # NOTE: STORING IEX TICKER VALUES
    """Creates ticker values table and stores ticker info each minute to the DB."""
    mk_table = """CREATE TABLE IF NOT EXISTS ticker_info_2 (
                group_timestamp integer not null,
                end_price float(2) not null,
                end_volume int null);"""
    cur.execute(mk_table)
    conn.commit()
    cur.execute("""INSERT INTO ticker_info_2 (group_timestamp, end_price, end_volume)
                VALUES (%s, %s, %s)""",
                (ticker_info.start_time, ticker_info.end_price, ticker_info.end_volume))
    conn.commit()


# SECTION: MAIN
params = db_config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

reddit = make_reddit()
chart_data = ChartVal()

scrape_reddit(reddit)
