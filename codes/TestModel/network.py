import networkx as nx
import shelve


class Network:
    """社交网络图类

    Attributes:
        graph: 图
        nodeNum: 节点个数
        edgeNum: 边个数
        connected_components: 连通分量集合列表
        connectedNum: 连通分量个数
        connectedMax: 最大连通分量大小
    """

    def __init__(self):
        self.graph = nx.Graph()
        self.graph.add_edges_from(eval(open('edges', encoding='utf-8').readline()))
        self.nodeNum = self.graph.number_of_nodes()
        self.edgeNum = self.graph.number_of_edges()
        self.connected_components = list(nx.connected_components(self.graph))
        self.connectedNum = len(list(self.connected_components))
        self.connectedMax = max(self.connected_components, key=len)
        self.clustering = self.cluster_coefficient()
        self.prank = self.page_rank() 
        self.central = self.centrality()

        # open('connected_components', 'w').write(str(self.connected_components))
        # open('clustering', 'w').write(str(self.clustering))
        # open('prank', 'w').write(str(self.prank))
        # open('central', 'w').write(str(self.central))

    def __str__(self):
        return 'Nodes: ' + str(self.nodeNum) + '\nEdges:' + str(self.edgeNum) + '\nConnected: ' + str(self.connectedNum)

    def page_rank(self):
        """PageRank算法
        Returns
        -------
        out : 存储图PageRank值的字典
        """
        newgraph = self.graph.to_directed()
        prank=nx.pagerank(newgraph,alpha=0.85)
        tops = sorted(prank.items(),  key=lambda x: x[1], reverse=True)
        return tops

    def cluster_coefficient(self):
        """节点聚集系数
        Returns
        -------
        out : 存储图聚集系数的字典
        """
        return nx.clustering(self.graph)

    def centrality(self):
        """图的中心性计算
        in: G
        out: degree_centrality, in_degree_centrality, out_degree_centrality
        """
        centrals = nx.degree_centrality(self.graph)
        tops = sorted(centrals.items(),  key=lambda x: x[1], reverse=True)
        return tops
    
    def get_top(self, n, k=10):
        """节点n关系最强的k个邻居
        Returns
        -------
        out : 存储前k个邻居的列表
        """
        neighbours = sorted(list(self.graph[n]), key=lambda x: self.graph[n][x]['w'], reverse=True)
        if len(neighbours) < k:
            return neighbours
        return neighbours[:k]

    def get_cluster(self, n):
        """节点n的聚集系数
        Returns
        -------
        out : float值
        """
        try:
            return self.clustering[n]
        except:
            return 0.0
        
    def get_rank(self, n):
        """节点n的PageRank
        Returns
        -------
        out : float值
        """
        try:
            return self.prank[n]
        except:
            return 0.0

    def get_central(self, n):
        """节点n的中心性
        Returns
        -------
        out : float值
        """
        try:
            return self.central[n]
        except:
            return 0.0


network = shelve.open('temp')['g']
print(network.nodeNum)
