import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.idMapOrders = {}
        self.idMapStores = {}
        self.bestPath = []


    def getAllStores(self):
        stores = DAO.getAllStores()
        for store in stores:
            self.idMapStores[store.store_id] = store
        return stores

    def buildGraph(self, store_id, k):
        self.graph.clear()
        store = self.idMapStores[store_id]
        orders = DAO.getOrdersByStore(store)
        for order in orders:
            self.idMapOrders[order.order_id] = order
        self.graph.add_nodes_from(orders)

        couples = DAO.getCouples(store, self.idMapOrders)
        edges = []
        for c in couples:
            d = int((c[1].order_date-c[0].order_date).days)
            if d <= k:
                weight = c[2]/d
                edges.append((c[0], c[1], weight))

        self.graph.add_weighted_edges_from(edges)

    def get5Heaviest(self):
        edges = list(self.graph.edges(data=True))
        edges.sort(key=lambda x: x[2]["weight"], reverse=True)
        return edges[:5]

    def getLongestPath(self, src_id):
        src = self.idMapOrders[int(src_id)]
        tree = nx.dfs_tree(self.graph, src)
        path = []
        for n in list(tree.nodes):
            temp = [n]
            while temp[0] != src:
                pred = nx.predecessor(tree, src, temp[0])
                temp.insert(0, pred[0])
            if len(temp) > len(path):
                path = copy.deepcopy(temp)

        return path

    def getHeaviestPath(self, src_id):
        src = self.idMapOrders[int(src_id)]
        self.bestPath = []
        partial = [src]
        for n in self.graph.successors(src):
            partial.append(n)
            self.ricorsione(partial)
            partial.pop()

        return self.bestPath

    def ricorsione(self, partial):
        if self.peso(partial) > self.peso(self.bestPath):
            self.bestPath = copy.deepcopy(partial)

        for n in self.graph.successors(partial[-1]):
            if self.graph.get_edge_data(partial[-1], n)["weight"] < self.graph.get_edge_data(partial[-2], partial[-1])["weight"]:
                partial.append(n)
                self.ricorsione(partial)
                partial.pop()

    def peso(self, path):
        if len(path) < 2:
            return 0
        peso = 0
        for i in range(len(path) - 1):
            peso += self.graph.get_edge_data(path[i], path[i + 1])["weight"]
        return peso









