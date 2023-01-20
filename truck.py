class Truck:
    truck1 = []
    truck2 = []
    truck3 = []

    total_delivery_time_truck1 = 0
    total_delivery_miles_truck1 = 0.0

    total_delivery_time_truck2 = 0
    total_delivery_miles_truck2 = 0.0

    total_delivery_time_truck3 = 0
    total_delivery_miles_truck3 = 0.0

    def __init(self, pkgs):
        self.packages = pkgs
    
    def load_packages_to_truck1(self, pkgs):
        Truck.load_to_truck(pkgs, self.truck1)

    def load_packages_to_truck2(self, pkgs):
        Truck.load_to_truck(pkgs, self.truck2)

    def load_packages_to_truck3(self, pkgs):
        Truck.load_to_truck(pkgs, self.truck3)

    # Time complexity:  O(N) >> where n is the max size of the number of packages in the pkgs list
    # Space complexity: O(N) >> a new list truck is created and adds the packages from pkgs list to it.
    @staticmethod
    def load_to_truck(pkgs, truck):
        if pkgs is not None:
            for pkg in pkgs:
                if pkg.get('status') != 'en route' and len(truck) < 16:
                    truck.append(pkg)
                    pkg.update({'status': 'en route'})
