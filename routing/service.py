
from .graph import load_graph
from .a_star import a_star_routing 
from .distance_matrix import matrix_loader
import networkx as nx

def compute_route(G, stop_nodes):
    # stores nodes to given index 
    index_to_node = {i: node for i, node in enumerate(stop_nodes)}

    # MATRIX CREATION 
    matrix = matrix_loader(stop_nodes, G)

    # CALCULATING TOTAL DISTANCE + ROUTE 
    g1, route_indices = a_star_routing(
        start_node=0,
        stop_nodes=list(range(len(stop_nodes))),
        distance_matrix=matrix
    )

    route_nodes = [index_to_node[i] for i in route_indices]

    g1 = round(float(g1), 2)

    # CONVERTING ORDERED STOPS TO FULL PATH
    full_path = [] 

    for i in range(len(route_nodes) - 1):
        segment = nx.shortest_path(
            G,
            route_nodes[i],
            route_nodes[i + 1],
            weight="'length"
        )

        if i > 0:
            segment = segment[i:]
        
        full_path.extend(segment)

    return g1, full_path