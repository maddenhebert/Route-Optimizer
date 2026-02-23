from Stop import Stop
from graph import load_graph
from a_star import a_star_routing 
from distance_matrix import matrix_loader
import random

def compute_route():
    # GRAPH LOADING 
    G = load_graph("Chicago, Illinois, USA")

    # NODE AND STOP CREATION 
    # takes G (map graph) and creates randon sample of given nodes
    stop_nodes = random.sample(list(G.nodes), 20)

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

    return {
        "total_distance": g1,
        "route": route
    }

print(compute_route())