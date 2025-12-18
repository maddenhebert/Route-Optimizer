import csv
import data_structures.hash_table as ht
import objects.package as p 
import datetime as dt
import objects.truck as t
import logistics.routing as routing
import logistics.package_statuses as ps
import logistics.total_mileage as tm

# DSA II - WGUPS Routing Program 
#Student ID: 012600680

# DATA PREP AND LOADING 
# instantiates hash table with capacity of 40
packages_table = ht.hash_table(40)

# opens csv file with package data
with open("wgups/csv/packages.csv") as packages:
    reader = csv.reader(packages) 

    # for each row, data is stored in variables and a package is made 
    for row in reader:
        package_id = int(row[0])
        address = row[1]
        city = row[2]
        state = row[3]
        zip_code = row[4]
        deadline = row[5]
        weight = int(row[6])
        special_notes = row[7]

        # creates package object and inserts into hash table
        package = p.package(package_id, address, city, state, zip_code, deadline, weight, special_notes)
        packages_table.insert(package_id, package)
        
# address to index for distance lookup, read from csv file  
with open('wgups/csv/addresses.csv') as addresses:
    reader = csv.reader(addresses)

    address_dict = {}
    index = 0

    for row in reader:
        address_dict[row[0]] = index
        index += 1

# opens csv file with distance data
with open('wgups/csv/distances.csv') as distances:
    reader = csv.reader(distances)

    # 2d list used for distance lookups 
    distance_matrix = []

    for row in reader:
        distance_row = []
        for item in row:
            if item == '':
                distance_row.append("")
            else:
                distance_row.append(float(item))
        distance_matrix.append(distance_row)

# lists for each truck's packages 
TruckLoad1 = [1, 7, 13, 14, 15, 16, 19, 20, 21, 27, 29, 34, 35, 39] # leaves first
TruckLoad2 = [2, 3, 4, 5, 6, 18, 25, 26, 36, 37, 38, 40, 31, 32, 33] # slightly Delayed for some packages
TruckLoad3 = [8, 9, 28, 10, 11, 12, 17, 22, 23, 24, 30] # waits for one truck to finish

# RUNNING ROUTES 
# formatted times for truck departures
departure1 = dt.datetime(2023, 1, 1, 8, 0)
departure2 = dt.datetime(2023, 1, 1, 9, 5)
departure3 = dt.datetime(2023, 1, 1, 10, 20) # earliest truck 3 can leave

# instantiate trucks 
truck1 = t.truck(1, departure1, TruckLoad1)
truck2 = t.truck(2, departure2, TruckLoad2)

# event log to track + sort deliveries 
event_log = []

# routing of frist two trucks 
completion_time1 = routing.nearest_neighbor(truck1, distance_matrix, address_dict, event_log, packages_table)
completion_time2 = routing.nearest_neighbor(truck2, distance_matrix, address_dict, event_log, packages_table)

# logic for deciding when truck 3 leaves
fastest_truck = min(completion_time1, completion_time2)
departure3 = max(fastest_truck, departure3)

# sets truck three now that we know its departure time
truck3 = t.truck(3, departure3, TruckLoad3)

# shortest time between trucks will be continued by truck 3
routing.nearest_neighbor(truck3, distance_matrix, address_dict, event_log, packages_table)

# total mileage calculation
total_mileage = truck1.mileage + truck2.mileage + truck3.mileage

# sort event log by time 
event_log.sort(key = lambda x: x["time"])

# USER INTERFACE 
program = True
while program == True:
    print('''\n   WGUPS Routing Program
    1) View Entire Delivery Log
    2) View Total Mileage
    3) View Package Statuses by Time
    4) Exit Program
    Input desired option below:\n'''
    )

    user_input = input().strip()

    # filters output based on user input 
    if user_input == "1":
        # formats and prints all events in order with time and truck
        print("Delivery Log:")
        for event in event_log:
            print(f"Truck {event['truck_id']} has delivered package {event['package_id']} at {event['time']} with {event['mileage']} miles.")
        print("\nWould you like to return to the interface? (y/n)")
        choice = input().lower().strip()
        if choice != 'y':
            program = False
            print("\nExiting Program")

    # displays total mileage
    elif user_input == "2":
        print(f"\nTotal mileage for all trucks is: {truck1.mileage + truck2.mileage + truck3.mileage} miles.")
        print("\nWould you like to return to the interface? (y/n)")
        choice = input().lower().strip()
        if choice != 'y':
            program = False
            print("\nExiting Program")

    # gives statuses of all packages at a certain time 
    elif user_input == "3":
        while True:
            print("\nEnter a time in HH::MM format (24 hour clock):\n")
            selected_time = input()

            # input validation for datetime
            try:
                selected_time = dt.datetime.strptime(selected_time, "%H:%M")
                selected_time = selected_time.replace(year=2023, month=1, day=1)
                break

            except ValueError:
                print("\nInvalid Time Format, enter time in HH:MM.\n")

        # functioin to get statuses at a given time 
        statuses = ps.package_statuses(packages_table, selected_time, event_log, truck1, truck2, truck3, packages_table)

        total_mileage = tm.get_total_mileage(event_log, selected_time)

        # formats selected time 
        time_str = selected_time.strftime("%H:%M")

        # prints all status messages
        print(f"\nPackage statuses at {time_str}:\n")
        for status_message in statuses:
            print(statuses[status_message])
        
        # prints total mileage
        print(f"Total Mileage at this time: {total_mileage}")

        # return prompt 
        print("\nWould you like to return to the interface? (y/n)")
        choice = input().lower().strip()
        if choice != 'y':
            program = False
            print("\nExiting Program")
            
    # exists program
    elif user_input == "4": 
        program = False
        print("\nExiting Program")