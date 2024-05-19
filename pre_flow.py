from collections import deque
from generate_graph import create_random_graph
from read_from_file import create_graph_from_file

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

  def push(self, u, edge):
      v = edge.to
      flow = min(self.excess[u], edge.capacity - edge.flow)
      edge.flow += flow
      edge.residual.flow -= flow
      self.excess[u] -= flow
      self.excess[v] += flow
      if v != self.sink and v != self.source and v not in self.queue:
          self.queue.append(v)

  def relabel(self, u):
      min_height = float('inf')
      for edge in self.graph.adj[u]:
          if edge.capacity > edge.flow:
              min_height = min(min_height, self.height[edge.to])
      self.height[u] = min_height + 1

  def discharge(self, u):
      while self.excess[u] > 0:
          for edge in self.graph.adj[u]:
              if edge.capacity > edge.flow and self.height[u] == self.height[edge.to] + 1:
                  self.push(u, edge)
                  if self.excess[u] == 0:
                      break
          else:
              self.relabel(u)

  def run(self):
      while self.queue:
          u = self.queue.popleft()
          self.discharge(u)

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



    
# Можно либо считать данные из файла
# graph = create_graph_from_file('tests/test_1.txt')
# или создать рандомный с 10 вершинами и 15 ребрами (чуть больше вообще-то между нами говоря)
# graph = create_random_graph(10, 15)

# print('lil maxflow: ', pre_flow(graph))