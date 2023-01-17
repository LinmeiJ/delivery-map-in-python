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

    total_time_all_trucks = 0
    total_mile_all_trucks = 0

    def __init(self, pkgs):
        self.packages = pkgs
    
    def load_packages_to_truck1(self, pkgs):
        if pkgs is not None and len(self.truck1) < 16:
            for pkg in pkgs:
                if pkg.get('status') != 'en route':
                    self.truck1.append(pkg)
                    pkg.update({'status': 'en route'})

    def load_packages_to_truck2(self, pkgs):
        if pkgs is not None:
            for pkg in pkgs:
                if pkg.get('status') != 'en route' and len(self.truck2) < 16:
                    self.truck2.append(pkg)
                    pkg.update({'status': 'en route'})

    def load_packages_to_truck3(self, pkgs):
        if pkgs is not None:
            for pkg in pkgs:
                if pkg.get('status') != 'en route' and len(self.truck3) <  16:
                    self.truck3.append(pkg)
                    pkg.update({'status': 'en route'})
