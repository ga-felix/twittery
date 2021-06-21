from api import api
from settings import settings
from database.sql import sql
import time

a = api.Api()
db = sql.Sql("twitter", "root", "zxc12989")

def download_user_timeline():
    for user in settings.user_timeline:
        pages = a.user_timeline(user, npages=1, max_results=25)

        for page in pages:
            for tweet in page.data:
                db.insertTweet(tweet)

            for tweet in page.includes.tweets:
                db.insertTweet(tweet)
                if hasattr(tweet, "mentions"):
                    pass
                if hasattr(tweet, "referenced_tweets"):
                    print(tweet)
                    for ref_tweet in tweet.referenced_tweets:
                        if ref_tweet.type == "replied_to":
                            db.insertReply(tweet.id, ref_tweet.id)
                        if ref_tweet.type == "quoted":
                            db.insertQuote(tweet.id, ref_tweet.id)
                        if ref_tweet.type == "retweeted":
                            db.insertRetweet(tweet.id, ref_tweet.id)

def foo():
    count = 0

    download_user_timeline()

if __name__ == "__main__":
    foo()