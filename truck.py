class Truck:
    # Initialize three empty trucks
    truck1 = []
    truck2 = []
    truck3 = []

    def __init__(self, pkgs):
        self.packages = pkgs

    def load_cargo(self, pkg_urgent_list, pkg_flight_delay_list, remaining_pkg):
        # Load packages with special notes
        self.load_cargo_by_special_notes()

        # Load urgent packages to the trucks who will go out first in the morning: truck1 and truck2
        self.load_cargo_by_urgent_package(pkg_flight_delay_list, pkg_urgent_list)
        self.load_cargo_by_remaining_package(remaining_pkg)

    def load_cargo_by_urgent_delivery(self, pkg_flight_delay_list, pkg_urgent_list):
        for pkg in pkg_urgent_list:
            # Truck2 plans to deliver a package requires deadline 9AM, then comes back to pick up the remaining delayed packages
            # meanwhile leave room for delayed packages
            if (vars(pkg[1]).get('deadline') == '9:00 AM' or (vars(pkg[1]).get('pid') == 6) and len(self.truck2)) < (
                    16 - len(pkg_flight_delay_list)):
                self.truck2.append(pkg)
                continue
            # if truck1 is not full and the package has not loaded it yet
            if len(self.truck1) < 16 and self.truck1.count(pkg) < 0:
                self.truck1.append(pkg)

    # special notes: 1) package 3 & 18 & 36 & 38: Can 0nly be on truck 2 and deadline is EOD
    #    2) package 6 & 25 & 28 & 32: Delayed on flight -> will not arrive to depot until 9:05 am but pkg 6 & 25 also require to be delivered before 10:30AM (urgent)
    #    3) package 9: Wrong address listed
    #    4) package 14: Must be delivered with 15, 19,
    #    5) package 16: Must be delivered with 13, 19
    #    6) package 20: Must be delivered with 13, 15
    #       (^package 14, 13, 15, 16, 19, 20 must be at the same truck^)
    def load_cargo_by_special_notes(self):
        for bucket in self.packages.table:
            for index, pkg in enumerate(bucket):
                if pkg[0] == 13 or pkg[0] == 14 or pkg[0] == 15 or pkg[0] == 16 or pkg[0] == 19 or pkg[0] == 20:
                    self.truck1.append(vars(pkg[1]))
                # set truck2 come back to the HUB for delaying pkgs
                if pkg[0] == 3 or pkg[0] == 18 or pkg[0] == 36 or pkg[0] == 38 or pkg[0] == 6 or pkg[0] == 25 or pkg[0] == 28 or pkg[0] == 32:
                    self.truck2.append(vars(pkg[1]))

    # trucks travel at a speed of 18 miles/hr, leave hub no earlier than 8:00AM
    def calc_time_travel(self, travel_miles):  # fix me
        pass
