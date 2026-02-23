import networkx as nx

# creates distance matrix from given nodes
def matrix_loader(nodes, graph):
    n = len(nodes)
    matrix = [[0] * n for _ in range(n)] 

    for i, src in enumerate(nodes):
        lengths = nx.single_source_dijkstra_path_length(graph, src, weight="length")

        for j, dst in enumerate(nodes):
            if i != j:
                matrix[i][j] = lengths.get(dst, float('inf'))
    
    return matrix