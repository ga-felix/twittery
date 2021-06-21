from api import api
from settings import settings
from database.sql import sql
from datetime import datetime
import time

a = api.Api()
db = sql.Sql("twitter", "root", "zxc12989")

def download_user_timeline():
    for user in settings.user_timeline:
        pages = a.user_timeline(user, npages=2, max_results=25)
        for page in pages:
            for tweet in page.data:
                db.insertTweet(tweet)
                if hasattr(tweet, "referenced_tweets"):
                    for referenced_tweet in tweet.referenced_tweets:
                        if referenced_tweet.type == "replied_to":
                            db.insertReply(tweet.id, referenced_tweet.id)
                        if referenced_tweet.type == "quoted":
                            db.insertQuote(tweet.id, referenced_tweet.id)
                        if referenced_tweet.type == "retweeted":
                            db.insertRetweet(tweet.id, referenced_tweet.id)
                        print(referenced_tweet)
def foo():
    count = 0

    download_user_timeline()

if __name__ == "__main__":
    foo()