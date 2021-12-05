from abc import ABC, abstractmethod
import networkx as nx
from database.sql import sql

class Graph(ABC):

    """ Global variables and export path """
    
    path = "reporter/reports/"
    db = sql.Sql("twitterDB", "root", "zxc12989")

    """ Implements default graph algorithm """

    def draw(self, gname, since='2000-01-01', until='2060-01-01'):
        self.graph = nx.Graph()
        self.since = since
        self.until = until
        self.nodes = self.get_nodes()
        self.add_edges()
        self.export(gname)

    """ Returns collection of nodes """

    @abstractmethod
    def get_nodes():
        pass

    """ Creates graph edges and nodes alongside """

    @abstractmethod
    def add_edges():
        pass

    """ Exports graph to 'path' """

    def export(self, gname):
        nx.write_gexf(self.graph, self.path + gname + ".gexf")