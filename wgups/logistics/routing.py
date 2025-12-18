# ROUTING FUNCTIONS
# Distance Calculating Function 

import datetime as dt

# function for getting distance between two addresses
def get_distance(package_address, current_address, distance_matrix, address_dict):
    destination_index = address_dict[package_address]
    current_index = address_dict[current_address]

    distance = distance_matrix[destination_index][current_index]
    if distance == "":
        distance = distance_matrix[current_index][destination_index]

    return float(distance)

# Nearest Neighbor Routing Function 
def nearest_neighbor(truck, distance_matrix, address_dict, event_log, packages_table):
    # at function start address is HUB
    current_address = truck.location

    # while there are still packages on the truck
    while truck.packages:
        # ensures there will be a shorter distance
        shortest_distance = float('inf')
        next_address = None

        # loop for finding package with shortest distance to address 
        for package_id in truck.packages:
            package = packages_table.lookup(package_id)
            package_address = package.address
            distance = get_distance(package_address, current_address, distance_matrix, address_dict)

            if distance < shortest_distance:
                shortest_distance = distance
                next_address = package_address

        # list to hold all packages at next address 
        packages_to_deliver = []

        # loop for finding all packages at the next address 
        for package_id in truck.packages:
            package = packages_table.lookup(package_id)
            if next_address == package.address:
                packages_to_deliver.append(package)

        # updates package status and remove from truck 
        for package in packages_to_deliver: 
            package.status = "Delivered"
            truck.packages.remove(package.package_id)

        # time calculations and formatting 
        travel_time = shortest_distance / 18
        travel_time = dt.timedelta(hours=travel_time)
        truck.time += travel_time

        # adds mileage to truck 
        truck.mileage += shortest_distance
        truck.mileage = round(truck.mileage, 2)
        
        # updates current location
        truck.location = next_address

        # prints completion message/s with time 
        for package in packages_to_deliver:
            event_log.append({
                "truck_id" : truck.truck_id,
                "time" : truck.time,
                "mileage" : truck.mileage,
                "package_id" : package.package_id,
                "status" : package.status 
            })

    ''' print when truck is finished (removed for UI purposes) 
    print(f"Truck {truck.truck_id} has completed deliveries at {truck.time} with total mileage of {truck.mileage} miles.")'''
    return truck.time 