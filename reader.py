def create_graph_from_file(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        num_vertices, num_edges = map(int, first_line.split())

        for vertex in range(1, num_vertices + 1):
            graph[vertex] = []

        for _ in range(num_edges):
            edge = file.readline().strip()
            start_vertex, end_vertex, capacity = map(int, edge.split())
            graph[start_vertex].append((end_vertex, capacity))

    return {'graph': graph, 'source': 1, 'sink': num_vertices}
