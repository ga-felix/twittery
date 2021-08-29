# -*- coding: utf-8 -*-

from api import api
from settings import settings
from database.sql import sql
import time
from tqdm import tqdm

""" Singleton references to api and database """

a = api.Api()
db = None

def insert_retweeters(page):
    if hasattr(page, 'data'):
        for retweeter in page.data:
            db.insertAccount(retweeter)

""" Insert users from twitter page """

def insert_users(page):
    if hasattr(page, "includes") and hasattr(page.includes, "users"):
        for user in page.includes.users:
            db.insertAccount(user)

""" Insert tweets from twitter page """

def insert_tweets(page):
    if hasattr(page, "data"):
        for tweet in page.data:
            db.insertTweet(tweet)
            print(tweet.id)
            if hasattr(tweet, "referenced_tweets"):
                for ref_tweet in tweet.referenced_tweets:
                    if ref_tweet.type == "replied_to":
                        db.insertReply(tweet.id, ref_tweet.id)
                    if ref_tweet.type == "quoted":
                        db.insertQuote(tweet.id, ref_tweet.id)
                    if ref_tweet.type == "retweeted":
                        db.insertRetweet(tweet.id, ref_tweet.id)


""" Insert referenced tweets (see expansions) from twitter page """

def insert_referenced_tweets(page):
    if hasattr(page, "includes") and hasattr(page.includes, "tweets"):
        for tweet in page.includes.tweets:
            print('inserting', str(tweet.text))
            db.insertTweet(tweet)
            
""" Extract data from a page """

def extract_page(page):
    insert_referenced_tweets(page)
    insert_tweets(page)
    insert_users(page)

""" Download user's timeline tweets """

def download_user_timeline(npages = -1, max_results = 50):
    global db
    db = sql.Sql("twitter", "root", "zxc12989")
    for user in settings.user_timeline:
        pages = a.user_timeline(user, npages = npages, max_results = max_results)
        for page in pages:
            extract_page(page)
    db.close()

def download_recent_tweets(query, npages = 1, max_results = 50):
    global db
    db = sql.Sql("twitter", "root", "zxc12989")
    pages = a.search_tweets(query, npages = npages, max_results = max_results)
    for page in pages:
        extract_page(page)
    db.close()

def download_historical_tweets(query, start_time=None, end_time=None, npages = 1, max_results = 50):
    global db
    db = sql.Sql("twitter", "root", "zxc12989")
    pages = a.full_search(query, start_time=start_time, end_time=end_time, npages = npages, max_results = max_results)
    for page in pages:
        extract_page(page)
    db.close()

def download_retweeters(id):
    global db
    db = sql.Sql("twitter", "root", "zxc12989")
    for page in a.retweeters_of(id):
        insert_retweeters(page)
        insert_referenced_tweets(page)
    db.close()