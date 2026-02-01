import datetime as dt

# function for aquiring all package statuses at a given time 
def package_statuses(packages_table, selected_time, event_log, truck1, truck2, truck3, package_table):
    status = {}

    # extracts the delivery time from each package event 
    delivery_times = {event["package_id"] : event["time"] for event in event_log}

    # adds time and dictionary for fast lookup of delayed packages
    flight_packages = {6, 25, 28, 32} 
    flight_arrival = dt.datetime.combine(selected_time, dt.time(9, 5))
    address_update = dt.datetime.combine(selected_time, dt.time(10,20))

    # loops through every package id
    for package_id in range(1, 41):

        # retrieves package object 
        package = package_table[package_id]

        # this sequence of conditionals checks which truck the package is on, and finds departure time 
        if package_id in truck1.starting_load:
            departure = truck1.departure_time
            truck = "Truck 1" 

        elif package_id in truck2.starting_load:
            departure = truck2.departure_time
            truck = "Truck 2"

        elif package_id in truck3.starting_load:
            departure = truck3.departure_time
            truck = "Truck 3"
        
        # extracts delivery time for package 
        delivery_time = delivery_times.get(package_id, None)
        if delivery_time:
            str_time = delivery_time.strftime("%H:%M")

        # formats package_id for smoothe output 
        if package_id < 10:
            pck_str = f"0{package_id}"
        
        else:
            pck_str = package_id

        # checks for package 9 address change 
        if package_id == 9 and selected_time >= address_update:
            package.address = "410 S State St"

        # these conditionals check time constraints to determine package status 
        # checks for flight packages
        if selected_time < flight_arrival and package_id in flight_packages:
            status[package_id] = f"Package {pck_str} on flight until 9:05 am -------- Deadline: Package to be delivered to {package.address} by {package.deadline}"

        # checks for packages at HUB
        elif selected_time < departure:
            status[package_id] = f"Package {pck_str} at HUB on {truck} -------------- Deadline: Package to be delivered to {package.address} by {package.deadline}"

        # checks for delivered packages
        elif delivery_time <= selected_time:
            status[package_id] = f"Package {pck_str} Delivered at {str_time} on {truck} -- Deadline: Package to be delivered to {package.address} by {package.deadline}"

        # checks for en route packages
        else:
            status[package_id] = f"Package {pck_str} En Route on {truck} ------------ Deadline: Package to be delivered to {package.address} by {package.deadline}"

    return status 