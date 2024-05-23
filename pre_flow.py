from collections import deque
from generator import create_random_graph
from reader import create_graph_from_file


# Вспомогательный код

class Edge:
    def __init__(self, from_, to, capacity):
        self.from_ = from_
        self.to = to
        self.capacity = capacity
        self.flow = 0
        self.residual = None  # ссылка на обратное ребро


class Graph:
    def __init__(self, num_vertices):
        self.adj = [[] for _ in range(num_vertices)]
        self.edges = {}

    def add_edge(self, from_, to, capacity):
        if (from_, to) in self.edges:
            self.edges[(from_, to)].capacity += capacity
        else:
            forward_edge = Edge(from_, to, capacity)
            backward_edge = Edge(to, from_, 0)
            forward_edge.residual = backward_edge
            backward_edge.residual = forward_edge
            self.adj[from_].append(forward_edge)
            self.adj[to].append(backward_edge)
            self.edges[(from_, to)] = forward_edge
            self.edges[(to, from_)] = backward_edge

    def size(self):
        return len(self.adj)


class PushRelabel:
    def __init__(self, graph, source, sink):
        self.graph = graph
        self.source = source
        self.sink = sink
        self.excess = [0] * graph.size()
        self.height = [0] * graph.size()
        self.queue = deque()
        self.in_queue = [False] * graph.size()
        self.counter = 0  # Counter for operations to trigger global relabel
        self.initialize_preflow()

    def initialize_preflow(self):
        self.height[self.source] = self.graph.size()
        for edge in self.graph.adj[self.source]:
            edge.flow = edge.capacity
            edge.residual.flow = -edge.flow
            self.excess[edge.to] += edge.flow
            self.excess[self.source] -= edge.flow
            if edge.to != self.sink:
                self.queue.append(edge.to)
                self.in_queue[edge.to] = True

    def push(self, u, edge):
        v = edge.to
        flow = min(self.excess[u], edge.capacity - edge.flow)
        edge.flow += flow
        edge.residual.flow -= flow
        self.excess[u] -= flow
        self.excess[v] += flow
        if not self.in_queue[v] and v != self.source and v != self.sink:
            self.queue.append(v)
            self.in_queue[v] = True

    def relabel(self, u):
        min_height = float('inf')
        for edge in self.graph.adj[u]:
            if edge.capacity > edge.flow:
                min_height = min(min_height, self.height[edge.to])
        self.height[u] = min_height + 1

    def discharge(self, u):
        for edge in self.graph.adj[u]:
            if self.excess[u] <= 0:
                break
            if edge.capacity > edge.flow and self.height[u] == self.height[edge.to] + 1:
                self.push(u, edge)
        if self.excess[u] > 0:
            self.queue.append(u)
            self.in_queue[u] = True

    def global_relabel(self):
        queue = deque([self.sink])
        self.height = [float('inf')] * self.graph.size()
        self.height[self.sink] = 0
        while queue:
            u = queue.popleft()
            for edge in self.graph.adj[u]:
                if edge.residual.capacity > edge.residual.flow and self.height[edge.to] > self.height[u] + 1:
                    self.height[edge.to] = self.height[u] + 1
                    queue.append(edge.to)

    def run(self):
        while self.queue:
            u = self.queue.popleft()
            self.in_queue[u] = False
            old_height = self.height[u]
            self.relabel(u)
            if self.height[u] > old_height:
                self.global_relabel()
                self.counter = 0
            self.discharge(u)
            self.counter += 1
            if self.counter >= 0.5 * len(self.graph.adj):
                self.global_relabel()
                self.counter = 0


def create_graph_from_data(data):
    num_vertices = max(max(edge[0], edge[1]) for edge in sum(data['graph'].values(), [])) + 1
    graph = Graph(num_vertices)
    for u in data['graph']:
        for v, capacity in data['graph'][u]:
            graph.add_edge(u, v, capacity)
    return graph


# Функция, которая вычисляет maxflow на основе алгоритма предпотока
def pre_flow(data):
    source = data['source']
    sink = data['sink']
    graph = create_graph_from_data(data)
    algorithm = PushRelabel(graph, source, sink)
    algorithm.run()
    return sum(edge.flow for edge in graph.adj[source])


# Example usage:
# Можно либо считать данные из файла
# graph = create_graph_from_file('tests/test_1.txt')
# или создать рандомный с 10 вершинами и 15 ребрами (чуть больше вообще-то между нами говоря)
# graph = create_random_graph(10, 15)

# print('lil maxflow: ', pre_flow(graph))
