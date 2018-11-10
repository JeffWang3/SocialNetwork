#!/usr/bin/env python
import os
import sys
import networkx as nx

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
        self.prank, self.prankTop = self.page_rank()
        self.central, self.centralTop = self.centrality()

        open('connected_components', 'w').write(str(self.connected_components))
        open('clustering', 'w').write(str(self.clustering))
        open('prank', 'w').write(str(self.prank))
        open('central', 'w').write(str(self.central))

    def __str__(self):
        return 'Nodes: ' + str(self.nodeNum) + '\nEdges:' + str(self.edgeNum) + '\nConnected: ' + str(self.connectedNum)

    def page_rank(self):
        """PageRank算法
        Returns
        -------
        out : 存储图PageRank值的字典
        """
        prank = nx.pagerank(self.graph.to_directed(), alpha=0.85)
        tops = sorted(prank.items(),  key=lambda x: x[1], reverse=True)
        return prank, tops[:20]

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
        return centrals, tops[:10]
    
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
    
    '''
    def find_route(self, a, b):
        return list(nx.all_shortest_paths(self.graph, source= a,target=b))
    '''

    def find_route(self, a, b):
        """小世界理论中的节点路径查询
        Parameters
        ----------
        a, b : 两个人的名字

        Returns
        -------
        out : 两个人之间的前十条最优最短路径列表
        """
        k=10
        cnt = 0
        result = []
        result1=[]
        for i in range(1,2000):
            if cnt >= k:
                break
            ans =list (nx.all_simple_paths(self.graph,a,b,i))
            for path in ans:
                if len(path)-1 > i-1:
                    result.append(path)
                    cnt+=1
        i = 0
        while i < len(result):
            for j in range(i,len(result)):
                if j == len(result)-1:
                    break
                if len(result[j+1])>len(result[i]):
                    break
                else: j+=1
            dict1 = {}
            p = i
            for p in range(i,j+1):
                w = 0
                for q in range(0,len(result[p])-1):
                    w+= self.graph.get_edge_data(result[p][q],result[p][q+1])['w']
                dict1[p]=w
            tops = dict(sorted(dict1.items(),  key=lambda x: x[1], reverse=True))
            for order, length in tops.items():
                result1.append(result[order])
            i= j+1
        return (result1)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TinyWorld.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
