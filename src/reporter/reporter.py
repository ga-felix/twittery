from .graph.graphs.followers import Followers
from .graph.graphs.mentions import Mentions
from .graph.graphs.tweets import Tweets
from .graph.graphs.retweets import Retweets
from .graph.graphs.retweetssum import RetweetsSum
import csv

def create_graph(gname, since='2000-01-01', until='2060-01-01'):
    if gname == "followers":
        Followers().draw(gname, since=since, until=until)
    if gname == "tweets":
        Tweets().draw(gname, since=since, until=until)
    if gname == "mentions":
        Mentions().draw(gname, since=since, until=until)
    if gname == "retweets":
        Retweets().draw(gname, since=since, until=until)
    if gname == "retweetssum":
        RetweetsSum().draw(gname, since=since, until=until)

def export_tweets(tweets, name):
    with open(name + '.csv', 'w+', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
        for tweet in tweets:
            tweet.text.replace("\"", "'")
            writer.writerow(vars(tweet).values())