# GRAPH PLOTTING 
# plot the network
"""
import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox

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
"""