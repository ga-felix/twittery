#!/usr/bin/python
from ..graph import Graph
import pandas as pd
import networkx as nx

class Retweets(Graph):

    """ Returns list of retweets """

    def get_nodes(self):
        pass

    """ Creates graph edges and nodes alongside """

    def add_edges(self):
        retweets = self.db.getRetweets()
        for retweet in retweets:
            retweeted_account = retweet["text"].split(" ")[1].replace("@", "").replace(":", "")
            retweeter_account = self.db.getAccount(retweet["author_id"])["username"]
            if (retweeter_account, retweeted_account) in self.graph.edges():
                edge_data = self.graph.get_edge_data(retweeter_account, retweeted_account)
                self.graph.add_edge(retweeter_account, retweeted_account, weight=edge_data['weight'] + 1)
            else:
                self.graph.add_edge(retweeter_account, retweeted_account, weight=1)