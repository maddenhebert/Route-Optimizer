# ROUTING A* FUNCTIONS

import datetime as dt
import heapq

# Function for getting distance between two addresses
def get_distance(n1, n2, distance_matrix, node_to_index):
    return distance_matrix[node_to_index[n1]][node_to_index[n2]]

# Heuristic 
def heuristic(curr_node, remaining, distance_matrix, node_to_index):
    # handles goal state
    if not remaining:
        return 0
    
    remaining = list(remaining)

    # determines min distances
    min_start = min(
        get_distance(curr_node, n, distance_matrix, node_to_index)
        for n in remaining
    )

    # primms algorithm for MST
    mst = 0 
    visited = set()
    unvisited = set(remaining)

    current = unvisited.pop()
    visited.add(current)

    while unvisited:
        min_edge = float('inf')
        next_node = None

        for v in visited:
            for u in unvisited:
                dist = get_distance(v, u, distance_matrix, node_to_index)
                if dist < min_edge and dist != float('inf'):
                    min_edge = dist
                    next_node = u
            
        if next_node is None:
            return float('inf')
        
        mst += min_edge
        visited.add(next_node)
        unvisited.remove(next_node)
    
    return mst + min_start

# Path reconstruction
def reconstruct_path(parents, state):
    path = []
    
    # creates list of all stops in the optimal path 
    while state in parents:
        parent_state, prev_remaining, child_stop = parents[state]
        path.append(child_stop)
        state = (parent_state, prev_remaining)
    
    # path is made in reverse 
    path.reverse() 
    return path 

# A* routing structure 
def a_star_routing(start_node, stops, distance_matrix, node_to_index):
    # initial state
    remaining = frozenset(stop.node for stop in stops if stop.node != start_node)
    start_state = (start_node, remaining)

    pq = []
    parents = {}

    # initial values
    g_score = {start_state: 0}
    h = heuristic(start_node, remaining, distance_matrix, node_to_index)

    # intializes heap and pushes starting state
    heapq.heappush(pq, (h, 0, start_state))

    while pq:
        f, g, (curr_node, remaining) = heapq.heappop(pq) 

        # checks goal (no packages left)
        if not remaining:
            return g, reconstruct_path(parents, (curr_node, remaining)) 
        
        for next_node in remaining:
            # creates new remaining set and state 
            new_remaining = set(remaining)
            new_remaining.remove(next_node)
            new_remaining = frozenset(new_remaining)
            new_state = (next_node, new_remaining)

            # calculating new g score 
            new_g = g + get_distance(curr_node, next_node, distance_matrix, node_to_index)

            if new_state not in g_score or new_g < g_score[new_state]:
                g_score[new_state] = new_g
                h = heuristic(next_node, new_remaining, distance_matrix, node_to_index)
                f = new_g + h
                heapq.heappush(pq, (f, new_g, new_state))
                parents[new_state] = (curr_node, remaining, next_node)
            
    return float('inf')