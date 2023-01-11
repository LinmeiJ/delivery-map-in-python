class Truck:
    # Initialize three empty trucks
    truck1 = []
    truck2 = []
    truck3 = []
    temp_pkgs = []

    def __init__(self, urgent_list, urgent_delayed_list, not_urgent_delayed_list, wrong_address, truck2_only,
                 on_same_truck, remaining_packages):
        # self.route_for_all_packages = all_pkg
        self.package_urgent_list = urgent_list
        self.package_urgent_delayed_list = urgent_delayed_list
        self.package_not_urgent_delayed_list = not_urgent_delayed_list
        self.package_with_wrong_address = wrong_address
        self.package_with_truck2_only = truck2_only
        self.package_must_on_same_truck = on_same_truck
        self.package_remaining_packages = remaining_packages

    def load_cargo(self):
        # Load packages with special notes
        self.load_cargo_by_urgency()
        self.load_cargo_by_remaining_packages()

    def load_cargo_by_urgency(self):
        size = len(self.package_urgent_list)
        for i, pkg in enumerate(self.package_urgent_list):
            if i < (size/2):
                self.truck1.append(pkg)
            else:
                self.truck2.append(pkg)

        # there are a list of packages are also consider as urgent packages, so load them along with truck1
        for pkg in self.package_must_on_same_truck:
            if self.truck1.count(pkg) < 1:
                self.truck1.append(pkg)

    def load_cargo_by_remaining_packages(self):
        for pkg in self.package_with_truck2_only:
            self.truck2.append(pkg)
        for pkg in self.package_urgent_delayed_list:
            self.truck2.append(pkg)
        for pkg in self.package_not_urgent_delayed_list:
            if len(self.truck1) <= 16:
                self.truck1.append(pkg)
            else:
                self.truck3.append(pkg)
        for pkg in self.package_with_wrong_address:
            # Since there are only 2 drivers, load the wrong address to trucks3 as it is last one gonna leave the Hub
            self.truck3.append(pkg)
        for pkg in self.package_remaining_packages:
            if len(self.truck1) < 16:
                self.truck1.append(pkg)
            elif len(self.truck2) < 16:
                self.truck2.append(pkg)
            else:
                self.truck3.append(pkg)


    # Trucks travel at a speed of 18 miles/hr, leave hub no earlier than 8:00AM
    # def calc_time_travel(self, travel_miles):  # fix me
    #     pass


