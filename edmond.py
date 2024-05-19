from collections import deque, defaultdict


def bfs_capacity_path(graph, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        current_vertex = queue.popleft()

        for neighbor, capacity in graph[current_vertex]:
            if neighbor not in visited and capacity > 0:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = (current_vertex, capacity)
                if neighbor == sink:
                    return True
    return False


def edmonds_karp(data):
    graph = data['graph']
    source = data['source']
    sink = data['sink']

    max_flow = 0
    parent = {}
    residual_graph = defaultdict(list)

    for u in graph:
        for v, capacity in graph[u]:
            residual_graph[u].append([v, capacity])
            residual_graph[v].append([u, 0])

    while bfs_capacity_path(residual_graph, source, sink, parent):
        path_flow = float('Inf')
        s = sink

        while s != source:
            u, capacity = parent[s]
            path_flow = min(path_flow, capacity)
            s = u

        v = sink
        while v != source:
            u, _ = parent[v]
            for i in range(len(residual_graph[u])):
                if residual_graph[u][i][0] == v:
                    residual_graph[u][i][1] -= path_flow
            for i in range(len(residual_graph[v])):
                if residual_graph[v][i][0] == u:
                    residual_graph[v][i][1] += path_flow
            v = u

        max_flow += path_flow

    return max_flow
