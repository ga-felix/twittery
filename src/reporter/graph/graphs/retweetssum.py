#!/usr/bin/python
from networkx.algorithms.distance_regular import intersection_array
from ..graph import Graph
import pandas as pd
import networkx as nx

class RetweetsSum(Graph):

    """ Returns list of retweets """

    def get_nodes(self):
        csv = pd.read_csv("settings/targets/medias-profiles.csv", encoding='utf-8', sep=',')
        targets = list()
        for index, account in csv.iterrows():
                targets.append(account[1])
        return targets

    """ Creates graph edges and nodes alongside """

    def add_edges(self):
        for source in self.nodes:
            for target in self.nodes:
                if source == target:
                    continue
                intersection = self.db.find('SELECT author_id FROM tweet WHERE text LIKE \"%RT @{}%\" AND author_id IN (SELECT author_id FROM tweet WHERE text LIKE \"%RT @{}%\")'.format(source, target))
                if len(intersection) == 0:
                    continue
                print('Intersection between', source, 'and', target, 'of', str(len(intersection)), 'retweets')
                self.graph.add_edge(source, target, weight=len(intersection))