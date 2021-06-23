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
            self.db = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset='utf8mb4')
            self.cursor = self.db.cursor()
            self.clock = time.time()
            #print("SQL Database: Connection stablished! Welcome " + user + ".")
        except Exception as e:
            with open('log.txt', 'a+') as log:
                log.write(str(date.today()) + ": SQL Database reported an error: " + str(e) + " \n")
                log.write(traceback.format_exc())
    
    # Execute any query following maintenance procedures
    def query(self, query):
        try:
            self.cursor.execute(query)
        except Exception as e:
            self.db.rollback()
            with open('log-sql-db.txt', 'a+') as log:
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
        self.query("INSERT INTO tweet (id, text, created_at, author_id, like_count, retweet_count, reply_count, quote_count) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\") ON DUPLICATE KEY UPDATE id=\"{}\", text=\"{}\", created_at=\"{}\", author_id=\"{}\", like_count=\"{}\", retweet_count=\"{}\", reply_count=\"{}\", quote_count=\"{}\";".format
        (tweet.id, tweet.text.replace("\"", "'"), tweet.created_at.split("T")[0], tweet.author_id, tweet.public_metrics.like_count, tweet.public_metrics.retweet_count, tweet.public_metrics.reply_count, tweet.public_metrics.quote_count,
        tweet.id, tweet.text.replace("\"", "'"), tweet.created_at.split("T")[0], tweet.author_id, tweet.public_metrics.like_count, tweet.public_metrics.retweet_count, tweet.public_metrics.reply_count, tweet.public_metrics.quote_count))

    # Insert a twitter account
    def insertAccount(self, account):
        self.query("INSERT INTO account (id, username, description, followers_count, following_count, tweet_count, listed_count, verified, created_at) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\") ON DUPLICATE KEY UPDATE id=\"{}\", username=\"{}\", description=\"{}\", followers_count=\"{}\", following_count=\"{}\", tweet_count=\"{}\", listed_count=\"{}\", verified=\"{}\", created_at=\"{}\";".format
        (account.id, account.username, account.description.replace("\"", "'"), account.public_metrics.followers_count, account.public_metrics.following_count, account.public_metrics.tweet_count, account.public_metrics.listed_count, int(account.verified), account.created_at.split("T")[0],
        account.id, account.username, account.description.replace("\"", "'"), account.public_metrics.followers_count, account.public_metrics.following_count, account.public_metrics.tweet_count, account.public_metrics.listed_count, int(account.verified), account.created_at.split("T")[0]))

    # Delete tweets meeting certain conditions
    def deleteTweet(self, condition):
        self.query("DELETE FROM tweet WHERE " + condition)

    # Delete twitter accounts meeting certain conditions
    def deleteAccount(self, condition):
        self.query("DELETE FROM account WHERE " + condition)