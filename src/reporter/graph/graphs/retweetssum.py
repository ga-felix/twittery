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
                targets.append(account)
        return targets

    """ Creates graph edges and nodes alongside """

    def add_edges(self):
        for source in self.nodes:
            source_retweeters = self.db.find('SELECT author_id FROM tweet WHERE `text` LIKE \"%RT @{}%\"'.format(source))
            for target in self.nodes:
                target_retweeters = self.db.find('SELECT author_id FROM tweet WHERE `text` LIKE \"%RT @{}%\"'.format(target))
                intersection = [x for x in source_retweeters if x in target_retweeters]
                if len(intersection) == 0:
                    continue
                print('Intersection between', source, 'and', target, 'of', str(len(intersection)), 'retweets')
                self.graph.add_edge(source, target, weight=len(intersection))