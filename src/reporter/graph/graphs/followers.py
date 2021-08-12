#!/usr/bin/python
from ..graph import Graph

class Followers(Graph):

    """ Get collection account name """

    def get_name(self, collection):
        return collection.split("_tweets")[0]

    """ Returns collection of nodes """

    def get_list(self):
        names = list()
        collections = self.mongo.get_collections()
        for collection in collections:
            if collection.endswith("_tweets"):
                names.append(collection)
        return names

    """ Sign a node """

    def sign_node(self, node):
        jb = len(self.mongo.find_intersection(node, 'jairbolsonaro_followers_ids', since=self.since, until=self.until))
        lula = len(self.mongo.find_intersection(node, 'LulaOficial_followers_ids', since=self.since, until=self.until))
        self.graph.add_node(self.get_name(node), jb=jb, lula=lula, size=jb + lula)

    """ Creates graph edges and nodes alongside """

    def add_edges(self):
        for e1 in self.list:
            for e2 in self.list:
                if e1 not in self.graph.nodes:
                    self.sign_node(e1)
                if e2 not in self.graph.nodes:
                    self.sign_node(e2)
                inter = len(self.mongo.find_intersection(e1, e2, since=self.since, until=self.until))
                if inter != 0:
                    union = self.mongo.count(e1, self.since, self.until) + self.mongo.count(e2, self.since, self.until) - inter
                    self.graph.add_edge(self.get_name(e1), self.get_name(e2), weight=(inter / union) * 100)