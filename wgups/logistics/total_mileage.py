# function for returning the total mileage traveled by all trucks
def get_total_mileage(event_log, selected_time):
# holds value for total mileage
    total_mileage = 0
    largest_mileage = {}

    for event in event_log:
        if event["time"] <= selected_time:
            truck_id = event["truck_id"]
            mileage = event["mileage"]

            # 
            if truck_id not in largest_mileage or mileage > largest_mileage[truck_id]:
                largest_mileage[truck_id] = mileage
        
    # adds all of the largest mileages 
    for i in range(1,4):
        total_mileage += largest_mileage.get(i, 0)
    
    return total_mileage
