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
        writer.writerow(["id", "text", "created_at", "author_id", "author_name", "like_count", "retweet_count", "quote_count", "reply_count", "retweet_of_id", "quote_of_id", "reply_to_id"])
        for tweet in tweets:
            writer.writerow([tweet.id, tweet.text.replace("\"", "'"), tweet.created_at, tweet.author_id, tweet.author.name, tweet.public_metrics.like_count, tweet.public_metrics.retweet_count, tweet.public_metrics.quote_count, tweet.public_metrics.reply_count, tweet.retweet_of, tweet.quote_of, tweet.reply_of])