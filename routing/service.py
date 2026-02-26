from .Stop import Stop
from .graph import load_graph
from .a_star import a_star_routing 
from .distance_matrix import matrix_loader
import networkx as nx

def compute_route(G, stop_nodes):
    # initializes a stop for each node and precomputes distances in matrix 
    stops = [Stop(node) for node in stop_nodes]

    # stores index for each node 
    node_to_index = {stop.node: i for i, stop in enumerate(stops)}

    # MATRIX CREATION 
    matrix = matrix_loader(stop_nodes, G)

    # CALCULATING TOTAL DISTANCE + ROUTE 
    g1, route = a_star_routing(
        start_node=stops[0].node,
        stops=stops,
        distance_matrix=matrix,
        node_to_index=node_to_index)
    
    g1 = round(float(g1), 2)

    # CONVERTING ORDERED STOPS TO FULL PATH
    full_path = [] 

    for i in range(len(route) - 1):
        segment = nx.shortest_path(
            G,
            route[i],
            route[i + 1],
            weight="'length"
        )

        if i > 0:
            segment = segment[i:]
        
        full_path.extend(segment)

    return g1, full_path