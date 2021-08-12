# -*- coding: utf-8 -*-

from api import api
from settings import settings
from database.sql import sql
import time
from tqdm import tqdm

""" Singleton references to api and database """

a = api.Api()
db = sql.Sql("twitter", "root", "zxc12989")

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
            db.insertTweet(tweet)
            
""" Extract data from a page """

def extract_page(page):
    insert_referenced_tweets(page)
    insert_tweets(page)
    insert_users(page)

""" Download user's timeline tweets """

def download_user_timeline(npages = -1, max_results = 50):
    count = 0
    #pbar = tqdm(settings.user_timeline, leave=False)
    for user in settings.user_timeline:
        #pbar.set_description("Downloading user timeline: %s" % user)
        pages = a.user_timeline(user, npages = npages, max_results = max_results)
        for page in pages:
            extract_page(page)
            count += 1
            print("[EXTRACTOR] inserting page of", str(user))
        print("[EXTRACTOR]", str(count), "tweets were inserted from", str(user), ".")
        count = 0
    print("[EXTRACTOR] over.")

def download_recent_tweets(query, max_results = 10):
    pages = a.search_tweets(query, max_results = max_results)
    for page in pages:
        print(str(page.data))
        extract_page(page)

""" Test function """

def main():
    download_recent_tweets("Desfile")

if __name__ == "__main__":
    main()