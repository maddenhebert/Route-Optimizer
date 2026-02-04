from objects.Stop import Stop
import logistics.routing as routing
import time
import osmnx as ox
import networkx as nx
import random
import matplotlib.pyplot as plt

# execution time
start = time.perf_counter()

# DATA HANDLING 
# creates a selection of 40 random nodes form salt lake city driving network 
G = ox.graph_from_place("Salt Lake City, Utah, USA", network_type = "drive")
stop_nodes = random.sample(list(G.nodes), 20)

# initializes a stop for each node and precomputes distances in matrix 
stops = [Stop(node) for node in stop_nodes]

# stores index for each node 
node_to_index = {stop.node: i for i, stop in enumerate(stops)}

# distance matrix creation for nodes
n = len(stop_nodes)
matrix = [[0] * n for _ in range(n)] 

for i, src in enumerate(stop_nodes):
    lengths = nx.single_source_dijkstra_path_length(G, src, weight="length")

    for j, dst in enumerate(stop_nodes):
        if i != j:
            matrix[i][j] = lengths.get(dst, float('inf'))

# TESTING ALGORITHM AND VISUALS
starting_node = stops[0].node
g1, efficient_route = routing.a_star_routing(starting_node, stops, matrix, node_to_index)
end = time.perf_counter()
print(f'RUNTIME: {end - start:.6f} seconds')

# plot the network
fig, ax = ox.plot_graph(G, node_size=5, edge_linewidth=0.5, show = False, close = False)

# plot the stops
for node in stop_nodes:
    x, y = G.nodes[node]['x'], G.nodes[node]['y']
    ax.scatter(x, y, c='red', s=50)
plt.show()