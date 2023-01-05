class Truck:
    def __init__(self, truck_id, lastLocation=1, nextLocation=None, driver=None, miles=0):
        self.cargo = []
        self.id = truck_id
        self.last_location = lastLocation
        self.next_location = nextLocation
        self.driver = driver
        self.miles = miles