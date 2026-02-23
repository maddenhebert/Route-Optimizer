from Stop import Stop
from graph import load_graph
from a_star import a_star_routing 
import networkx as nx
import random
import matplotlib.pyplot as plt
import osmnx as ox

# GRAPH LOADING 
G = load_graph("Chicago, Illinois, USA")

# NODE CREATION 
# takes G (map graph) and creates randon sample of given nodes
stop_nodes = random.sample(list(G.nodes), 20)

# MATRIX CALCULATION 
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
g1, efficient_route = a_star_routing(starting_node, stops, matrix, node_to_index)

# GRAPH PLOTTING 
# plot the network
fig, ax = ox.plot_graph(G, node_size=5, edge_linewidth=0.5, show = False, close = False)

# plot the stops
for node in stop_nodes:
    x, y = G.nodes[node]['x'], G.nodes[node]['y']
    ax.scatter(x, y, c='red', s=50, edgecolors='black', zorder=6, marker='*')

# draw the efficient route if found
if efficient_route:
    route_edges = []
    for i in range(len(efficient_route) - 1):
        try:
            # Get the shortest path between consecutive nodes
            path = nx.shortest_path(G, efficient_route[i], efficient_route[i+1], weight='length')
            for j in range(len(path) - 1):
                if G.has_edge(path[j], path[j+1]):
                    route_edges.append((path[j], path[j+1], 0))
        except nx.NetworkXNoPath:
            print(f"No path found between {efficient_route[i]} and {efficient_route[i+1]}")
    
    # Plot the route
    if route_edges:
        ox.plot_graph_route(G, [edge[0] for edge in route_edges], ax=ax, route_color='blue', 
                           route_linewidth=3, route_alpha=0.5, orig_dest_size=0)

# add a title
ax.set_title(f'A* Routing Solution: {len(stops)} stops, Total Distance: {g1:.2f}m')
plt.show()