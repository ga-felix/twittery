#!/usr/bin/python
from ..graph import Graph
import pandas as pd
import networkx as nx

class Mentions(Graph):

    """ Returns list of retweets """

    def get_list(self):
        csv = pd.read_csv("settings/data/tweets.csv", encoding='utf-8', sep=';')
        retweets = list()
        for index, tweet in csv.iterrows():
            retweets.append(tweet)
        return retweets

    """ Creates graph edges and nodes alongside """

    def add_edges(self):
        accounts = set()
        for tweet in self.list:
            tweet_author = tweet["author"]
            if not tweet_author in accounts:
                    accounts.add(tweet_author)
                    self.graph.add_node(tweet_author, tweet_count=1)
            else:
                nx.set_node_attributes(self.graph, {tweet_author:self.graph.nodes[tweet_author]['tweet_count'] + 1}, 'tweet_count')
                    
        for a_acc in accounts:
            followers = self.api.call("followers_ids", a_acc, count=5000)
            for b_acc in accounts:
                if a_acc == b_acc:
                    continue
                if (a_acc, b_acc) in self.graph.edges() or (b_acc, a_acc) in self.graph.edges():
                    continue
                    #edge_data = self.graph.get_edge_data(a_acc, b_acc)
                    #self.graph.add_edge(a_acc, b_acc, weight=edge_data['weight'] + 1)
                else:
                    try:
                        id_b_acc = self.api.call("user", b_acc).id
                    except Exception:
                        print("Usuário ignorado " + b_acc)
                        continue
                    if id_b_acc in followers:
                        print("Amizade entre " + a_acc + " e " + b_acc)
                        self.graph.add_edge(a_acc, b_acc, weight=1)