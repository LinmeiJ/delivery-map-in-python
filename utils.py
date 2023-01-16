import copy
# from datetime import datetime, time
from datetime import datetime, timedelta

import graph
from Package import Package
from truck import Truck


class Utils:
    start_time = datetime.strptime("8:00 AM", "%I:%M %p")

    hub = vars(Package(0, '4001 South 700 East',
                       'Salt Lake City', 'UT', '84107', '', '', '', start_time, '', 0,
                       'placeholder-hub-location'))

    truck = Truck()

    def __init__(self):
        # Load packages from a csv file
        self.route1 = None
        self.route2 = None
        self.route3 = None

        self.pkgs = Package(0, '', '', '', '', '', '', '', '', '', '', False)  # Create an instance of Package
        self.pkgs.load_package_data()

        # Load graph data from a csv file
        self.graph = graph.Graph()

        self.list_of_pkgs = self.remove_keys_from_pkgs_table()

        self.pkg_loading_optimization()

    def remove_keys_from_pkgs_table(self):
        pkg_info = []
        for pkgs in self.pkgs.package_table.table:
            for pkg in pkgs:
                pkg_info.append(vars(pkg[1]))
        return pkg_info

    # Load cargo and return a route
    def load_more_packages(self, urgent_pkg_route, route, remaining_pkgs):
        remaining_pkg_list = []  # Initialize a temp list in case we need find fast route independently
        for pkg in remaining_pkgs:
            if len(self.truck.truck1) < 16:
                self.truck.truck1.append(pkg)
                remaining_pkg_list.append(pkg)
            else:
                break

        # Calculate a new route after combing all packages, set the Hub location as the beginning of the route
        new_route = self.find_fast_route(Utils.hub, self.truck.truck1)

        # Check if the fastest new route can also deliver urgent packages on time
        if Utils.can_delivery_on_time_for_all_pkg(
                Utils.calc_total_time_for_delivery(new_route)):
            return new_route
        else:
            new_route = self.calculate_route_based_on_urgency(remaining_pkg_list, urgent_pkg_route)
            return new_route

    def calculate_route_based_on_urgency(self, remaining_pkg_list, urgent_pkg_route):
        # Calculate the route for remaining pkgs based on the last pkg location in the urgent delivery route
        last_urgent_pkg_location = urgent_pkg_route[-1]
        # Check if there are addresses in remaining packages that are already contained in the urgent route
        Utils.remove_duplicated_location(urgent_pkg_route, remaining_pkg_list)
        # find a fast route based on the last urgent pkg location as starting point
        remaining_route = self.find_fast_route(last_urgent_pkg_location, remaining_pkg_list)
        remaining_route.remove(last_urgent_pkg_location)
        # Return a new route that combines both routes
        return urgent_pkg_route + remaining_route  # combine two routes as a final route

    @staticmethod
    def remove_duplicated_location(urgent_route, remaining_route):
        pkg_ids = []

        for rem_pkg in remaining_route:
            rem_address = rem_pkg.get('address') + ' ' + rem_pkg.get('zip_code')
            for i, pkg in enumerate(urgent_route):
                address = pkg.get('address') + ' ' + pkg.get('zip_code')
                if rem_address == address:
                    pkg_ids.append(rem_pkg['pid'])
                    urgent_route.insert(i + 1, rem_pkg)
                    break

        for i in range(len(remaining_route)-1, -1, -1):
            if remaining_route[i].get('pid') in pkg_ids:
                remaining_route.pop(i)

    def pkg_loading_optimization(self):
        # Always load the urgent delivery packages first
        route_for_urgent_pkgs = self.find_fast_route(Utils.hub, self.pkgs.package_urgent_list)

        # If one truck can carry all the urgent packages and can deliver one time, load to the truck1
        if Utils.can_delivery_on_time_for_all_pkg(
                Utils.calc_total_time_for_delivery(route_for_urgent_pkgs)):
            # Load urgent packages to truck1
            self.truck.load_packages_to_truck1(route_for_urgent_pkgs)

            # Truck's max capacity is 16
            if len(route_for_urgent_pkgs) == 16:
                self.route1 = route_for_urgent_pkgs
            elif len(route_for_urgent_pkgs) < 16:
                # Each time when call find_fast_route function, the returned the route adds hub location as the beginning of the route
                route_for_urgent_pkgs.remove(Utils.hub)
                self.truck.truck1.remove(Utils.hub)

                # Load more packages until truck1 is full and also set the final route for truck1
                self.route1 = self.load_more_packages(route_for_urgent_pkgs, self.route1,
                                                      self.pkgs.package_remaining_packages)

        # Split the packages into 2 trucks
        else:
            # find out how many urgent packages can one truck carry based on the latest delivery deadline at 10:30 AM
            num_of_pkgs = Utils.deliverable_packages(route_for_urgent_pkgs, Utils.start_time)

            # Split the urgent packages
            urgent_pkgs1 = route_for_urgent_pkgs[0:num_of_pkgs + 1]
            urgent_pkgs2 = route_for_urgent_pkgs[num_of_pkgs + 1:]

            # load them into truck1 and truck2

            # self.set_route1(urgent_pkgs1)
            # self.set_route2(urgent_pkgs2)

    # def set_route2(self, pkgs=None):
    #     self.truck.load_packages_to_truck2(pkgs)
    #     self.truck.load_packages_to_truck2(self.pkgs.package_with_truck2_only)
    #     self.truck.load_packages_to_truck2(self.pkgs.package_remaining_packages)
    #
    #     # Update package status to 'en route'
    #     self.update_pkg_status(self.truck.truck2, 'en route')
    #     self.route2 = self.find_fast_route(self.hub, self.truck.truck2)
    #     self.route2.remove(Utils.hub)

    # set route for truck1
    def set_route1(self, route_for_urgent_pkgs):
        self.truck.load_packages_to_truck1(route_for_urgent_pkgs)
        temp_list = []

        # add remaining packages until truck1 is full
        for pkg in self.pkgs.package_remaining_packages:
            if len(self.truck.truck1) < 16:
                self.truck.truck1.append(pkg)
                temp_list.append(pkg)
            else:
                break
        # Update package status to 'en route'
        self.update_pkg_status(self.truck.truck1, 'en route')
        self.route1 = self.recalculate_route_based_on_urgency(route_for_urgent_pkgs, temp_list)
        print('here')

    # This calculates how many packages a truck carries to delivery all urgent package on time based on urgent package list
    @staticmethod
    def deliverable_packages(packages, start_time):

        if not packages:  # check if it is empty
            return 0

        pkg = packages[0]
        time_elapsed = timedelta(hours=(pkg.get('travel_distance') / 18))  # Truck travels 18 miles per hour

        if start_time + time_elapsed <= datetime.strptime("10:30 AM",
                                                          "%I:%M %p"):  # the latest urgent package is at 10:30AM
            return 1 + Utils.deliverable_packages(packages[1:], start_time + time_elapsed)
        else:
            return 0

    def update_pkg_status(self, truck, status):
        for pkg in self.list_of_pkgs:
            if truck.count(pkg) > 0 and pkg.get('pid') != 0:
                pkg.update({'status': status})

    def delivery_packages(self):
        pass
        # return total_time, total_mile, final_route

    def exclude_delayed_pkgs(self):
        delayed_pkgs = self.pkgs.package_urgent_delayed_list + self.pkgs.package_not_urgent_delayed_list
        pkgs_in_hub = []
        for pkg in self.list_of_pkgs:
            if delayed_pkgs.count(pkg) > 0:
                continue
            else:
                pkgs_in_hub.append(pkg)
        return pkgs_in_hub

    def urgent_package_delivery_feasibility(self, route):
        first_route = []
        second_route = []
        third_route = []
        temp_pkg = []
        for pkg in route:
            if len(first_route) < 16:
                first_route.append(pkg)
            elif len(second_route) < 16:
                second_route.append(pkg)
            else:
                third_route.append(pkg)

        return first_route, second_route, third_route

    # TSP algorithm for planning a route for a fast delivery
    def find_fast_route(self, sta_location, p):
        packages = copy.deepcopy(p)
        # Initialize a route
        route = [sta_location]
        current_location = sta_location.get('address') + ' ' + sta_location.get('zip_code')
        nearest_address = ''
        # Keep looping until all locations have been visited
        while packages:
            # Find the nearest unvisited location to the current location
            nearest_location = None
            nearest_distance = float('inf')
            for pkg in packages:
                # if pkg['status'] == 'delivered':
                nearest_address = pkg['address'] + ' ' + pkg['zip_code']
                location_distance = self.calc_distance(current_location,
                                                       nearest_address)
                if location_distance != '' and location_distance is not None:
                    dist = float(location_distance)
                    if dist < nearest_distance:
                        nearest_location = pkg
                        nearest_distance = dist
            if nearest_location is not None:
                if self.is_same_address(nearest_address, current_location):
                    nearest_location.update({'travel_distance': 0})
                else:
                    nearest_location.update({'travel_distance': nearest_distance})
                route.append(nearest_location)

                # Remove the nearest location from the list of unvisited locations
                packages.remove(
                    nearest_location)
                # Set the current location to the nearest location
                current_location = nearest_location.get('address') + ' ' + nearest_location.get('zip_code')
        return route

    def calc_distance(self, address1, address2):
        for kv in self.graph.address_with_distance.items():
            if kv[0] == address1:
                for elem in kv[1]:
                    if elem[0] == address2:
                        return elem[1]

    @staticmethod
    def minute_per_mile():
        return float(60 / 18)

    @staticmethod
    def calc_total_time_for_delivery(packages_in_route):
        total_mile = 0
        for pkg in packages_in_route:
            total_mile += pkg.get('travel_distance')
        total_time = Utils.minute_per_mile() * total_mile
        return int(total_time)

    @staticmethod
    def can_delivery_on_time_for_all_pkg(estimate_time):
        if estimate_time > (60 * 2 + 30):  # start from 8AM to 10:30AM in minutes
            return False
        else:
            return True

    @staticmethod
    def is_same_address(pkg_address, current_location):
        if current_location == pkg_address:
            return True
        else:
            return False

    # def start_package_delivery(self, packages_in_route, total_time, total_miles, time_start_to_deliver, hub_location,
    #                            pkg9=None):
    #     Utils.update_package_status_to_en_route(packages_in_route)
    #     back_to_hub = copy.deepcopy(hub_location)
    #     packages_in_route.append(back_to_hub)
    #
    #     # Calculate the time back to Hub after delivered all packages
    #     last_package_location = packages_in_route[-2].get('address') + ' ' + packages_in_route[-2].get('zip_code')
    #     hub_address = packages_in_route[-1].get('address') + ' ' + packages_in_route[-1].get('zip_code')
    #     distance_to_hub = float(Utils.calc_distance(hub_address, last_package_location))
    #
    #     for pkg in packages_in_route:
    #         if pkg.get('status') == 'delivered' and pkg.get('pid') != 0:
    #             continue
    #         if pkg.get('pid') == 0:
    #             pkg.update({'travel_distance': distance_to_hub})
    #         dist = pkg.get('travel_distance')
    #         time_used, delivered_time = Utils.format_time(dist, time_start_to_deliver)
    #         pkg.update({'start_time': delivered_time})
    #         pkg.update({'delivery_time': delivered_time})
    #         pkg.update({'status': 'delivered'})
    #         time_start_to_deliver = delivered_time
    #         total_time += time_used
    #         total_miles += dist
    #         start_loc = pkg
    #         if pkg9 is not None and Utils.is_address_updated(pkg.get('delivery_time')):
    #             packages_in_route.remove(hub_location)
    #             Utils.update_package9_address(pkg9)
    #             Utils.packages_in_route.append(pkg9)
    #             new_route = Utils.find_fast_route(start_loc, packages_in_route)
    #             total_time, total_miles, packages_in_route = Utils.start_package_delivery(new_route, total_time,
    #                                                                                       total_miles,
    #                                                                                       start_loc.get(
    #                                                                                           'delivery_time'),
    #                                                                                       hub_location)
    #             break
    #
    #     # total_miles += round(distance_to_hub, 2)
    #
    #     # total_time = total_time + int(distance_to_hub * minute_per_mile())
    #
    #     return total_time, round(total_miles, 2), packages_in_route

    # @staticmethod
    # def calc_time(dist):
    #     time_used = int(dist * 60 / 18)  # total time in minutes used from current location to nearst location
    #     travel_in_hour = int(time_used / 60)  # convert to hour if time_used more than or equal 60 minutes
    #     if travel_in_hour != 0:
    #         travel_in_minute = int(time_used % 60)  # get the remaining minutes if time travel is over an hour
    #     else:
    #         travel_in_minute = time_used  # less than 60 minutes
    #     return time_used, travel_in_hour, travel_in_minute
    #
    # @staticmethod
    # def format_time(dist, start_time):
    #     format_str = '%I:%M %p'
    #     time_obj = datetime.strptime(start_time, format_str).time()
    #     hour = time_obj.hour
    #     minute = time_obj.minute
    #
    #     time_used, travel_in_hour, travel_in_minute = Utils.calc_time(dist)
    #
    #     update_hour = hour + travel_in_hour
    #     update_minute = minute + travel_in_minute
    #     if update_minute > 59:
    #         update_hour += int(update_minute / 60)
    #         update_minute %= 60
    #     new_time = time(update_hour, update_minute, 0)
    #
    #     return time_used, new_time.strftime('%I:%M %p')

    # @staticmethod
    # def update_package9_address(pkg):
    #     pkg.update({'address': '410 S State St'})
    #     pkg.update({'city': 'Salt Lake City'})
    #     pkg.update({'state': 'UT'})
    #     pkg.update({'zip_code': '84111'})

    # @staticmethod
    # def is_address_updated(leaving_hub_time):
    #     format_str = '%I:%M %p'
    #     time_obj = datetime.strptime(leaving_hub_time, format_str).time()
    #     hour = time_obj.hour
    #     minute = time_obj.minute
    #     # Package #9 >>> wrong address and its address will be updated at 10:20AM
    #     if hour > 10:
    #         return True
    #     elif hour == 10:
    #         if minute >= 20:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False
    #
    # @staticmethod
    # def remove_package(packages_truck3):
    #     for pkg in packages_truck3:
    #         if pkg.get('pid') == 9:
    #             packages_truck3.remove(pkg)
    #             break
    #         return pkg
    #
    # #
    # # def load_delayed_packages(truck2, truck3):
    # #     for pkg in self.package_urgent_delayed_list:
    # #         if len(truck2) < 16:
    # #             truck2.append(pkg)
    # #         else:
    # #             truck3.append(pkg)
    # #     for pkg in self.package_not_urgent_delayed_list:
    # #         if len(truck2) < 16:
    # #             truck2.append(pkg)
    # #         else:
    # #             truck3.append(pkg)

    # truck = Truck(pkgs.package_urgent_list, pkgs.package_urgent_delayed_list,
    #               pkgs.package_not_urgent_delayed_list, pkgs.package_with_wrong_address, pkgs.package_with_truck2_only,
    #               pkgs.package_must_on_same_truck,
    #               pkgs.package_remaining_packages)
    # truck.load_cargo()
    #
    # # despite package id 15 requires delivery at 9:00AM, based on the current route, it will deliver on time
    # truck1_total_time, truck1_total_mile, route1 = plan_and_deliver_packages(truck.truck1, "truck1",
    #                                                                          '08:00 AM')  # driver1
    # # let truck2 wait until 9:05 to leave the hub for loading the delayed packages
    # truck.load_delayed_packages()
    # truck2_total_time, truck2_total_mile, route2 = plan_and_deliver_packages(truck.truck2, "truck2",
    #                                                                          '09:05 AM')  # driver2
    # start_delivery_time = route1[-1].get('delivery_time')
    # truck3_total_time, truck3_total_mile, route3 = plan_and_deliver_packages(truck.truck3, "truck3",
    #                                                                          start_delivery_time)  # diver1
