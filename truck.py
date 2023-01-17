class Truck:
    truck1 = []
    truck2 = []
    truck3 = []

    total_delivery_time_truck1 = 0
    total_delivery_miles_truck1 = 0

    total_delivery_time_truck2 = 0
    total_delivery_miles_truck2 = 0

    total_delivery_time_truck3 = 0
    total_delivery_miles_truck3 = 0

    def __init(self, pkgs):
        self.packages = pkgs
    
    def load_packages_to_truck1(self, pkgs):
        self.load_to_truck(pkgs, self.truck1)

    def load_packages_to_truck2(self, pkgs):
        self.load_to_truck(pkgs, self.truck2)

    def load_packages_to_truck3(self, pkgs):
        self.load_to_truck(pkgs, self.truck3)

    def load_to_truck(self, pkgs, truck):
        if pkgs is not None:
            for pkg in pkgs:
                if pkg.get('status') != 'en route' and len(truck) < 16:
                    self.truck3.append(pkg)
                    pkg.update({'status': 'en route'})
