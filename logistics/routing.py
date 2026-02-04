# ROUTING A* FUNCTIONS

import datetime as dt
import heapq

# Function for getting distance between two addresses
def get_distance(package_address, curr_address, distance_matrix, address_dict):
    destination_index = address_dict[package_address]
    curr_index = address_dict[curr_address]

    distance = distance_matrix[destination_index][curr_index]
    if distance == "":
        distance = distance_matrix[curr_index][destination_index]

    return float(distance)

# Heuristic 
def heuristic(curr_address, remaining_packages, distance_matrix, address_dict, packages_table):
    # handles goal state
    if not remaining_packages:
        return 0
    
    addresses = []
    for pid in remaining_packages:
        package = packages_table[pid]
        addresses.append(package.address)
    
    # determines min distances
    min_start = float('inf')
    for addrs in addresses:
        dist = get_distance(addrs, curr_address, distance_matrix, address_dict)
        min_start = min(min_start, dist)

    # primms algorithm for MST
    mst = 0 
    visited = set()
    unvisited = set(addresses)

    current = unvisited.pop()
    visited.add(current)

    while unvisited:
        min_edge = float('inf')
        next_node = None

        for v in visited:
            for u in unvisited:
                dist = get_distance(v, u, distance_matrix, address_dict)
                if dist < min_edge:
                    min_edge = dist
                    next_node = u

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
def a_star_routing(truck, distance_matrix, address_dict, packages_table):
    # initial state
    start_state = (truck.location, frozenset(truck.packages))

    pq = []
    parents = {}

    # initial values
    g_score = {start_state : 0}
    h = heuristic(truck.location, truck.packages, distance_matrix, address_dict, packages_table)

    # intializes heap and pushes starting state
    heapq.heappush(pq, (h, 0, start_state))

    while pq:
        f, g, (curr_address, remaining) = heapq.heappop(pq) 

        # checks goal (no packages left)
        if not remaining:
            return g, reconstruct_path(parents, (curr_address, remaining)) 
        
        for next_stop in remaining:
            # creates new remaining set 
            new_remaining = set(remaining)
            new_remaining.remove(next_stop)
            new_remaining = frozenset(new_remaining)

            package = packages_table[next_stop]
            next_address = package.address
            new_state = (next_address, new_remaining)

            # calculating new g score 
            distance = get_distance(next_address, curr_address, distance_matrix, address_dict)
            new_g = g + distance 

            if new_state not in g_score or new_g < g_score[new_state]:
                g_score[new_state] = new_g
                h = heuristic(next_address, new_remaining, distance_matrix, address_dict, packages_table)
                f = new_g + h
                heapq.heappush(pq, (f, new_g, new_state))
                parents[new_state] = (curr_address, remaining, next_address)
            
    return float('inf')