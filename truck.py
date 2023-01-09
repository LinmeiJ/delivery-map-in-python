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
        for pkg in self.package_urgent_list:
            # Leave the earliest urgent package to truck2, as the driver need to go back to the Hub pick up the flight delayed but urgent delivery is also required.
            # Thus, truck1 can focus on get the remaining urgent packages delivered on time
            if pkg.get('deadline') == "9:00 AM":
                self.temp_pkg.append(pkg)
                continue
            self.truck1.append(pkg)

        # there are a list of packages are also consider as urgent packages, so load them along with truck1
        for pkg in self.package_must_on_same_truck:
            if self.truck1.count(pkg) < 1:
                self.truck1.append(pkg)

    def load_cargo_by_remaining_packages(self):
        for tp in self.temp_pkgs:
            self.truck2.append(tp)  # this is the package that requires to be delivered by 9AM
        for pkg in self.package_with_truck2_only:
            self.truck2.append(pkg)
        for pkg in self.package_urgent_delayed_list:
            self.truck2.append(pkg)
        for pkg in self.package_not_urgent_delayed_list:
            if len(self.truck2) >= 16:
                self.truck2.append(pkg)
            else:
                self.truck1.append(pkg)
        for pkg in self.package_with_wrong_address:
            self.truck3.append(pkg)   # Since there are only 2 drivers, load this 2 trucks to allow time for the address to be updated.
        for pkg in self.package_remaining_packages:
            if len(self.truck1) < 16:
                self.truck1.append(pkg)
            elif len(self.truck2) < 16:
                self.truck2.append(pkg)
            else:
                self.truck3.append(pkg)


    # # # trucks travel at a speed of 18 miles/hr, leave hub no earlier than 8:00AM
    # def calc_time_travel(self, travel_miles):  # fix me
    #     pass
