# -*- coding: utf-8 -*-

from ..database import Database
import traceback
import pymysql
import pymysql.cursors
from datetime import datetime
from datetime import date
import time

class Sql(Database):

    # Gets database driver and connect to it
    def __init__(self, db, user, password, host='localhost', port=3306):
        try:
            self.db = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.db.cursor()
            self.clock = time.time()
            print("SQL Database: Connection stablished! Welcome " + user + ".")
        except Exception as e:
            with open('logs/log.txt', 'a+') as log:
                log.write(str(date.today()) + ": SQL Database reported an error: " + str(e) + " \n")
                log.write(traceback.format_exc())

    def __enter__(self):
        return self

    def __exit__(self):
        self.db.commit()
        self.cursor.close()

    # Execute any query following maintenance procedures
    def query(self, query):
        try:
            self.cursor.execute(query)
        except Exception as e:
            self.db.rollback()
            with open('logs/log-sql-db.txt', 'a+') as log:
                log.write(str(date.today()) + ": SQL Database reported an error: " + str(e) + " \n" + " query: " + query)
                log.write(traceback.format_exc())
        else:
            now = time.time()
            if now - self.clock > 3:
                self.db.commit()
                self.clock = now

    # Stablishes a retweet relationship between two tweets
    def insertRetweet(self, retweeter, retweeted):
        self.query("INSERT IGNORE INTO retweet (id_retweeter, id_retweeted) VALUES (\"{}\", \"{}\");".format(retweeter, retweeted))

    # Stablishes a quote relationship between two tweets
    def insertQuote(self, quoter, quoted):
        self.query("INSERT IGNORE INTO quote (id_quoter, id_quoted) VALUES (\"{}\", \"{}\");".format(quoter, quoted))

    # Stablishes a reply relationship between two tweets
    def insertReply(self, replier, replied):
        self.query("INSERT IGNORE INTO reply (id_replier, id_replied) VALUES (\"{}\", \"{}\");".format(replier, replied))  

    # Insert a tweet
    def insertTweet(self, tweet):
        date = tweet.created_at.split("T")[0]
        text = tweet.text.replace("\"", "'")
        self.query("INSERT INTO tweet (id, text, created_at, author_id, like_count, retweet_count, reply_count, quote_count) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\") ON DUPLICATE KEY UPDATE id=\"{}\", text=\"{}\", created_at=\"{}\", author_id=\"{}\", like_count=\"{}\", retweet_count=\"{}\", reply_count=\"{}\", quote_count=\"{}\";".format
        (tweet.id, text, date, tweet.author_id, tweet.public_metrics.like_count, tweet.public_metrics.retweet_count, tweet.public_metrics.reply_count, tweet.public_metrics.quote_count,
        tweet.id, text, date, tweet.author_id, tweet.public_metrics.like_count, tweet.public_metrics.retweet_count, tweet.public_metrics.reply_count, tweet.public_metrics.quote_count))

    # Insert a twitter account
    def insertAccount(self, account):
        date = account.created_at.split("T")[0]
        description = account.description.replace("\"", "'")
        verified = int(account.verified)
        self.query("INSERT INTO account (id, username, description, followers_count, following_count, tweet_count, listed_count, verified, created_at) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\") ON DUPLICATE KEY UPDATE id=\"{}\", username=\"{}\", description=\"{}\", followers_count=\"{}\", following_count=\"{}\", tweet_count=\"{}\", listed_count=\"{}\", verified=\"{}\", created_at=\"{}\";".format
        (account.id, account.username, description, account.public_metrics.followers_count, account.public_metrics.following_count, account.public_metrics.tweet_count, account.public_metrics.listed_count, verified, date,
        account.id, account.username, description, account.public_metrics.followers_count, account.public_metrics.following_count, account.public_metrics.tweet_count, account.public_metrics.listed_count, verified, date))

    # Delete tweets meeting certain conditions
    def deleteTweet(self, condition):
        self.query("DELETE FROM tweet WHERE " + condition)

    # Delete twitter accounts meeting certain conditions
    def deleteAccount(self, condition):
        self.query("DELETE FROM account WHERE " + condition)

    #Request account
    def getAccount(self, id):
        self.query("SELECT * FROM account WHERE id = \"{}\"".format(id))
        return self.cursor.fetchone()

    # Request retweets
    def getRetweets(self):
        self.query("SELECT * FROM tweet, retweet WHERE id = id_retweeter")
        return self.cursor.fetchall()

    # Request retweeter's account
    def getRetweeters(self):
        self.query("SELECT * FROM account WHERE id IN (SELECT author_id FROM tweet, retweet WHERE tweet.id = retweet.id_retweeter)")
        return self.cursor.fetchall()

    # Request retweeted's account
    def getRetweeteds(self):
        self.query("SELECT * FROM account WHERE id IN (SELECT author_id FROM tweet, retweet WHERE tweet.id = retweet.id_retweeted)")
        return self.cursor.fetchall()

    # Match any query
    def find(self, query):
        self.query(query)
        return self.cursor.fetchall()