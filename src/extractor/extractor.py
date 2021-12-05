# -*- coding: utf-8 -*-
from api import api
#from database.sql import sql

class DataProcessor():

    def has_authors(self):
        return hasattr(self.page, "includes") and hasattr(self.page.includes, "users")

    def has_data(self):
        return hasattr(self.page, "data")

    def process_page_data(self):
        get_authors = self.has_authors()
        if self.has_data():
            for index, tweet in enumerate(self.page.data):
                if get_authors:
                    tweet.author = self.page.includes.users[index]
                self.tweets.append(tweet)
                
    def process_page(self, page):
        self.page = page
        self.tweets = list()
        self.process_page_data()
        return self.tweets

class Download():

    def __init__(self, dbms, database, user, password):
        self.connection = None
        if dbms.lower() == "mysql":
            self.connection = sql.Sql(database, user, password)
        if self.connection != None:
            self.t_api = api.Api()
            self.data = DataProcessor()

    def download_tweets(self, tweets):
        with self.connection:
            for tweet in tweets:
                self.connection.insertTweet(tweet)
                if hasattr(self.tweet, "author"):
                    self.connection.insertAccount(tweet.author)

    def download_user_timeline(self, users, npages=-1, max_results=50):
        for user in users:
            self.download_tweets(self.data.process_page(self.t_api.user_timeline(user, npages=npages, max_results=max_results)))

    def download_recent_tweets(self, query, npages=1, max_results=50):
        self.download_tweets(self.data.process_page(self.t_api.search_tweets(query, npages = npages, max_results = max_results)))

    def download_historical_tweets(self, query, start_time=None, end_time=None, npages=1, max_results=100):
        self.download_tweets(self.data.process_page(self.t_api.full_search(query, start_time=start_time, end_time=end_time, npages=npages, max_results=max_results)))

class Lookup():

    def __init__(self):
        self.t_api = api.Api()
        self.data = DataProcessor()
    
    def get_first_tweet(self, keywords, lang="pt", start_time="2006-03-21T12:51:00Z", end_time=None):
        query = str()
        for keyword in keywords:
            query += "(\"" + keyword + "\")" + " OR "
        query = query[:len(query) - 3]
        print(query)
        #tweets = self.data.process_page(self.t_api.full_search(query, start_time=start_time, end_time=end_time, npages=npages, max_results=max_results))
