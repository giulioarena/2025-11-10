import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.idMapOrders = {}
        self.idMapStores = {}

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










