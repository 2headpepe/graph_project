from collections import deque

class PushRelabel:
    def __init__(self, graph, source, sink):
        self.graph = graph
        self.source = source
        self.sink = sink
        self.size = len(graph) + 1
        self.excess = [0] * self.size
        self.height = [0] * self.size
        self.queue = deque()
        self.in_queue = [False] * self.size
        self.flow_network = self.initialize_flow_network()

    def queue_pop(self):
        u = self.queue.popleft()
        self.in_queue[u] = False
        return u

    def queue_push(self, u):
        self.queue.append(u)
        self.in_queue[u] = True
        return u

    def initialize_flow_network(self):
        flow_network = {}
        for u in self.graph:
            flow_network[u] = {}
            for v, capacity in self.graph[u]:
                if v not in flow_network:
                    flow_network[v] = {}
                flow_network[u][v] = {'capacity': capacity}
                if u not in flow_network[v]:
                    flow_network[v][u] = {'capacity': 0}
        self.ensure_reverse_edges(flow_network)
        return flow_network

    @staticmethod
    def ensure_reverse_edges(flow_network):
        for u in flow_network:
            for v in flow_network[u]:
                if u not in flow_network[v]:
                    flow_network[v][u] = {'capacity': 0}

    def initialize_preflow(self):
        self.height[self.source] = self.size
        for neighbor in self.flow_network[self.source]:
            capacity = self.flow_network[self.source][neighbor]['capacity']
            if capacity <= 0:
                continue
            if neighbor != self.sink:
                self.queue_push(neighbor)

            self.flow_network[self.source][neighbor]['capacity'] = 0
            self.flow_network[neighbor][self.source]['capacity'] += capacity
            self.excess[neighbor] = capacity
            self.excess[self.source] -= capacity


    def relabel(self, u):
        min_height = float("inf")
        for v in self.flow_network[u]:
            if self.flow_network[u][v]['capacity'] > 0:
                min_height = min(min_height, self.height[v])
        if min_height < float("inf"):
            self.height[u] = min_height + 1

    def perform_push(self, u, v):
        if self.excess[u] < self.flow_network[u][v]['capacity']:
            flow = self.excess[u]
        else: 
            flow = self.flow_network[u][v]['capacity']
        self.flow_network[u][v]['capacity'] -= flow
        self.flow_network[v][u]['capacity'] += flow
        self.excess[u] -= flow
        self.excess[v] += flow

    def manage_queue(self, v):
        if not self.in_queue[v] and v != self.source and v != self.sink:
            self.queue_push(v)

    def check_push(self, u, v):
        if self.flow_network[u][v]['capacity'] > 0 and self.height[u] > self.height[v]:
            self.perform_push(u, v)
            self.manage_queue(v)
        
    def discharge(self, u):
        for v in self.flow_network[u]:
            if self.excess[u] == 0:
                break
            self.check_push(u, v)

        if self.excess[u] > 0:
            self.queue_push(u)

    def compute_max_flow(self):
        self.initialize_preflow()
        while self.queue:
            u = self.queue_pop()

            self.relabel(u)
            self.discharge(u)

        return self.excess[self.sink]

def pre_flow(data):
    algorithm = PushRelabel(data['graph'], data['source'], data['sink'])

    max_flow = algorithm.compute_max_flow()
    return max_flow
