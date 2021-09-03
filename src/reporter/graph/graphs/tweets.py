#!/usr/bin/python
from ..graph import Graph
import pandas as pd
import networkx as nx

class Tweets(Graph):

    """ Returns list of retweets """

    def get_nodes(self):
        csv = pd.read_csv("settings/targets/tweets.csv", encoding='utf-8', sep=',')
        retweets = list()
        for index, tweet in csv.iterrows():
            if tweet["text"].lower().startswith("rt @") == True:
                retweets.append(tweet)
        return retweets

    """ Creates graph edges and nodes alongside """

    def add_edges(self):
        edges = dict()
        tweet_number = 0 # Contagem de aparição na amostra
        for tweet in self.nodes:
            tweet_author = tweet["author"] # Autor do tweet
            tweet_rt_author = tweet["retweeted_screen_name"] # Nome do autor original
            if not tweet_author in edges: # Se o autor não está registrado, registre
                edges[tweet_author] = {}
            if not tweet_rt_author in edges[tweet_author]:
                edges[tweet_author][tweet_rt_author] = 1
            if tweet_rt_author in self.graph.nodes:
                nx.set_node_attributes(self.graph, {tweet_rt_author:self.graph.nodes[tweet_rt_author]['tweet_count'] + 1}, 'tweet_count')
                tweet_number += 1
            else:
                self.graph.add_node(tweet_rt_author, tweet_count=1)
                tweet_number += 1

        temp = list()
        for author in edges:
            for rt_first_author in edges[author]:
                for rt_second_author in edges[author]:
                    if rt_second_author in temp:
                        continue
                    if (rt_first_author, rt_second_author) in self.graph.edges():
                        edge_data = self.graph.get_edge_data(rt_first_author, rt_second_author)
                        self.graph.add_edge(rt_first_author, rt_second_author, weight=edge_data['weight'] + 1)
                    else:
                        if rt_first_author != rt_second_author:
                            self.graph.add_edge(rt_first_author, rt_second_author, weight=1)
                            temp.append(rt_first_author)
            temp.clear()
