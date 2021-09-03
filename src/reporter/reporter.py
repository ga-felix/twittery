from abc import ABC, abstractmethod
import networkx as nx
from database.sql import sql
from .graph.graphs.followers import Followers
from .graph.graphs.mentions import Mentions
from .graph.graphs.tweets import Tweets
from .graph.graphs.retweets import Retweets
from .graph.graphs.retweetssum import RetweetsSum

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