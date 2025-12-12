class truck:
    def __init__(self, truck_id, time, packages):
        self.truck_id = truck_id
        self.time = time 
        self.packages = packages
        self.mileage = 0.0
        self.location = "HUB" # default starting location

    