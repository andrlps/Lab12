import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.dizRetailer = {}
        self._graph = None
        self.edges = []

    def builGraph(self, anno, nazione):
        for ret in DAO.getRetailers(nazione):
            self.dizRetailer[ret.Retailer_code] = ret
        self._graph = nx.Graph()
        self._graph.add_nodes_from(self.dizRetailer.values())
        self.edges = DAO.getAllEdges(nazione, anno)
        for e in self.edges:
            self._graph.add_edge(self.dizRetailer[e.r1], self.dizRetailer[e.r2], weight=e.weight)

    def getInfoGraph(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getVolumeVendita(self):
        if self._graph is None:
            return None
        volume = []
        for node in self._graph.nodes():
            vol = 0
            for nod in self._graph.neighbors(node):
                vol+= self._graph[node][nod]["weight"]
            volume.append((node, vol))
        volume.sort(key = lambda x:x[1], reverse=True)
        return volume

    def percorso(self):
        pass