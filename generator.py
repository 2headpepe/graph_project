import networkx as nx
import random


def create_directed_graph_with_source_and_sink(n, m, U):
    G = nx.gnm_random_graph(n - 2, m, directed=True)

    source = n - 2
    sink = n - 1
    G.add_node(source)
    G.add_node(sink)

    num_source_edges = random.randint(1, n - 3)
    for target in range(n - 2):
        if num_source_edges == 0:
            break
        G.add_edge(source, target)
        num_source_edges -= 1

    num_sink_edges = random.randint(1, n - 3)
    for source_node in range(n - 2):
        if num_sink_edges == 0:
            break
        G.add_edge(source_node, sink)
        num_sink_edges -= 1

    for (u, v) in G.edges():
        G.edges[u, v]['capacity'] = random.randint(1, U)

    return G


def can_reach_source_to_sink(graph, source, sink):
    visited = set()

    def dfs(node):
        visited.add(node)
        if node == sink:
            return True
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
        return False

    return dfs(source)


def create_random_nx_graph(n, m, U):
    while True:
        graph = create_directed_graph_with_source_and_sink(n, m, U)
        source = n - 2
        sink = n - 1
        if can_reach_source_to_sink(graph, source, sink):
            return graph


def create_random_graph(n, m, U):
    graph = create_random_nx_graph(n, m, U)
    result = {}
    for start_vertex in graph.nodes():
        edges = []
        for end_vertex in graph.neighbors(start_vertex):
            capacity = graph[start_vertex][end_vertex]['capacity']
            edges.append((end_vertex, capacity))
        result[start_vertex] = edges
    return {'graph': result, 'source': n - 2, 'sink': n - 1}


def change_graph_capacity(graph, U):
    for (u, v) in graph.edges():
        graph.edges[u, v]['capacity'] = random.randint(1, U)