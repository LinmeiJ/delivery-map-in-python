import copy
import math
from datetime import datetime, timedelta, time

import graph
from Package import Package
from truck import Truck


class Utils:

    today = datetime.today().date()
    leaving_time = time(8, 0)
    start_time = datetime.combine(today, leaving_time)

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
        self.delivery_packages()

        print(len(self.truck.truck1))
        print(self.truck.truck1)
        print(
            f'miles in total: {self.truck.total_delivery_miles_truck1}  and time in total: {self.truck.total_delivery_time_truck1}')

        print(len(self.truck.truck2))
        print(self.truck.truck2)
        print(
            f'miles in total: {self.truck.total_delivery_miles_truck2}  and time in total: {self.truck.total_delivery_time_truck2}')

        print(len(self.truck.truck3))
        print(self.truck.truck3)
        print(
            f'miles in total: {self.truck.total_delivery_miles_truck3}  and time in total: {self.truck.total_delivery_time_truck3}')

    def remove_keys_from_pkgs_table(self):
        pkg_info = []
        for pkgs in self.pkgs.package_table.table:
            for pkg in pkgs:
                pkg_info.append(vars(pkg[1]))
        return pkg_info

    # Load cargo and return a route
    def load_more_packages(self, urgent_pkg_route, truck, pkgs1, pkgs2, space_size):
        remaining_pkg_list = []  # Initialize a temp list in case we need find fast route independently

        # Optional.... different type of pkgs
        if pkgs1 is not None:
            for pkg in pkgs1:
                if pkg.get('status') != 'loaded':
                    truck.append(pkg)
                    pkg.update({'status': 'loaded'})
                    remaining_pkg_list.append(pkg)

        for pkg in pkgs2:
            if pkg.get('status') != 'loaded':
                if len(truck) < 16:
                    truck.append(pkg)
                    pkg.update({'status': 'loaded'})
                    remaining_pkg_list.append(pkg)
                else:
                    break

        # Calculate a new route after combing all packages, already set the Hub location as the beginning of the route
        new_route = self.find_fast_route(Utils.hub, truck)

        # Check if the fastest new route can also deliver urgent packages on time
        if Utils.can_delivery_on_time_for_all_pkg(
                Utils.calc_total_time_for_delivery(new_route)):
            truck.clear()
            truck.extend(new_route)
            return new_route
        else:
            new_route = self.calculate_route_based_on_urgency(remaining_pkg_list, urgent_pkg_route)
            truck.clear()
            truck.extend(new_route)
            return new_route

    def append_hub_as_final_destination(self, route):
        hub_location = copy.deepcopy(Utils.hub)
        current_address = route[-1].get('address') + ' ' + route[-1].get('zip_code')
        travel_distance = self.drive_back_hub(current_address)
        hub_location.update({'travel_distance': travel_distance})
        route.append(hub_location)

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

        for i in range(len(remaining_route) - 1, -1, -1):
            if remaining_route[i].get('pid') in pkg_ids:
                remaining_route.pop(i)

    def update_packages_status_loaded(self, pkgs):
        for pkg in self.pkgs.package_urgent_list:
            for p in pkgs:
                if pkg.get('pid') == p.get('pid'):
                    pkg.update({'status': 'loaded'})
                    break

        for pkg in self.pkgs.package_must_on_same_truck:
            for p in pkgs:
                if pkg.get('pid') == p.get('pid'):
                    pkg.update({'status': 'loaded'})
                    break

    def pkg_loading_optimization(self):
        # Always load the urgent delivery packages first
        route_for_urgent_pkgs = self.find_fast_route(Utils.hub,
                                                     self.pkgs.package_urgent_list + self.pkgs.package_must_on_same_truck)

        # If one truck can carry all the urgent packages and can deliver one time, load to the truck1
        if Utils.can_delivery_on_time_for_all_pkg(
                Utils.calc_total_time_for_delivery(route_for_urgent_pkgs)) and len(route_for_urgent_pkgs) <= 16:
            # load truck1
            self.get_route_by_full_load_truck1(route_for_urgent_pkgs)

        # Split the packages into 2 trucks
        else:
            self.set_route_by_splitting_urgent_packages(route_for_urgent_pkgs)

        # Load truck2
        # If there is no urgent packages
        if len(self.truck.truck2) == 0:
            self.truck.load_packages_to_truck2(self.pkgs.package_with_truck2_only)
            if len(self.truck.truck2) < 16:
                self.truck.load_packages_to_truck2(self.pkgs.package_remaining_packages)
        else:
            self.truck.load_packages_to_truck2(self.pkgs.package_with_truck2_only)
            if len(self.truck.truck2) >= 16:
                print("You may need to hire more drivers")
            else:
                self.truck.load_packages_to_truck2(self.pkgs.package_remaining_packages)
        self.set_route2()

        # Load truck3  (since there are only 40 packages, the truck3 won't exceed its capacity)
        self.truck.load_packages_to_truck3(self.pkgs.package_with_wrong_address)
        self.truck.load_packages_to_truck3(self.pkgs.package_remaining_packages)

        self.route3 = self.find_fast_route(Utils.hub,
                                           self.truck.truck3)  # fix me, the leaving hub time for truck3 will be the time when truck 1 comes back

    def set_route2(self):
        route = self.find_fast_route(Utils.hub, self.truck.truck2)
        if Utils.can_delivery_on_time_for_all_pkg(
                Utils.calc_total_time_for_delivery(route)):
            self.route2 = route

            self.truck.truck2.clear()
            self.truck.truck2.extend(route)
        else:
            self.find_new_route()

    def find_new_route(self):
        urgent_pkgs = []
        remaining_pkgs = []
        for pkg in self.truck.truck2:
            if pkg.get('deadline') != 'EOD':
                urgent_pkgs.append(pkg)
            else:
                remaining_pkgs.append(pkg)

        urgent_pkg_route = self.find_fast_route(Utils.hub, urgent_pkgs)
        remaining_pkg_route = self.find_fast_route(urgent_pkg_route[-1], remaining_pkgs)
        remaining_pkg_route.remove(urgent_pkg_route[-1])

        new_route = urgent_pkg_route + remaining_pkg_route
        self.route2 = new_route

        self.truck.truck2.clear()
        self.truck.truck2.extend(new_route)

    def get_route_by_full_load_truck1(self, route_for_urgent_pkgs):
        # Update packages status to loaded
        self.update_packages_status_loaded(route_for_urgent_pkgs)

        # Load more packages to truck1
        self.truck.load_packages_to_truck1(route_for_urgent_pkgs)

        # Truck's max capacity is 16
        if len(self.truck.truck1) == 16:
            self.route1 = route_for_urgent_pkgs

        elif len(self.truck.truck1) < 16:
            self.route1 = self.load_partial_truck_and_get_route(route_for_urgent_pkgs, self.truck.truck1,
                                                                None,
                                                                self.pkgs.package_remaining_packages)

    # Make sure some packages must be on a same truck
    def split_packages(self, max_hold, max_size):
        rest_count = max_size - max_hold
        urgent_pkgs1 = []
        urgent_pkgs2 = []
        size = len(self.pkgs.package_must_on_same_truck)
        max_hold -= size
        count = 0
        for pkg in self.pkgs.package_must_on_same_truck:
            urgent_pkgs1.append(pkg)
            pkg.update({'status': 'loaded'})

        if max_hold != 0:
            for pkg in self.pkgs.package_remaining_packages:
                if count < max_hold:
                    urgent_pkgs1.append(pkg)
                    pkg.update({'status': 'loaded'})
                elif rest_count == 0:
                    break

                urgent_pkgs2.append(pkg)
                pkg.update({'status': 'loaded'})
                count += 1
                rest_count -= 1
        return urgent_pkgs1, urgent_pkgs2

    def set_route_by_splitting_urgent_packages(self, route_for_urgent_pkgs):
        # find out how many urgent packages can one truck carry based on the latest delivery deadline at 10:30 AM
        num_of_pkgs = Utils.deliverable_packages_count(route_for_urgent_pkgs, Utils.start_time)
        # Split the urgent packages, load truck1 first
        urgent_pkgs1, urgent_pkgs2 = self.split_packages(num_of_pkgs, len(route_for_urgent_pkgs))

        self.truck.load_packages_to_truck1(self.find_fast_route(Utils.hub, urgent_pkgs1))
        self.update_packages_status_loaded(urgent_pkgs1)

        # Load and make sure truck1 is full
        if len(self.truck.truck1) < 16:
            self.route1 = self.load_partial_truck_and_get_route(urgent_pkgs1, self.truck.truck1,
                                                                self.pkgs.package_must_on_same_truck,
                                                                self.pkgs.package_remaining_packages)

        else:
            self.route1 = urgent_pkgs1

        self.truck.truck1.clear()
        self.truck.truck1.extend(self.route1)

        # Load the rest of urgent delivery packages to truck2
        self.route2 = self.truck.load_packages_to_truck2(self.find_fast_route(Utils.hub, urgent_pkgs2))
        self.update_packages_status_loaded(urgent_pkgs2)
        # if len(self.truck.truck2) < 16:
        #     space_size_for_delayed_pkgs = len(self.pkgs.package_urgent_delayed_list) + len(
        #         self.pkgs.package_not_urgent_delayed_list)
        #     self.route2 = self.load_partial_truck_and_get_route(urgent_pkgs2, self.truck.truck2,
        #                                                         self.pkgs.package_remaining_packages,
        #                                                         self.pkgs.package_with_truck2_only,
        #                                                         space_size_for_delayed_pkgs)

    def load_partial_truck_and_get_route(self, route_for_urgent_pkgs, truck, pkgs1, pkgs2, space_size=0):
        # Load more packages until truck1 is full and also set the final route for truck1
        return self.load_more_packages(route_for_urgent_pkgs, truck, pkgs1, pkgs2, space_size)

    # This calculates how many packages a truck carries to delivery all urgent package on time based on urgent package list
    @staticmethod
    def deliverable_packages_count(packages, start_time):
        #  check if it is empty
        if not packages:
            return 0

        pkg = packages[0]
        time_elapsed = timedelta(hours=(pkg.get('travel_distance') / 18))  # Truck travels 18 miles per hour

        if start_time + time_elapsed <= datetime.strptime("10:30 AM",
                                                          "%I:%M %p"):  # the latest urgent package is at 10:30AM
            return 1 + Utils.deliverable_packages_count(packages[1:], start_time + time_elapsed)
        else:
            return 0

    # TSP algorithm for planning a route for a fast delivery
    def find_fast_route(self, sta_location, p):
        packages = copy.deepcopy(p)
        # Initialize a route
        if sta_location.get('pid') == 0:
            sta_location.update({'distance': 0})
        route = []
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
                location_distance = self.calc_distance(current_location, nearest_address)
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

    def calc_distance(self, start, end):
        for kv in self.graph.address_with_distance.items():
            if kv[0] == start:
                for elem in kv[1]:
                    if elem[0] == end:
                        return elem[1]

    @staticmethod
    def minute_per_mile():
        return float(60 / 18)

    @staticmethod
    def calc_total_time_for_delivery(packages_in_route):
        total_mile = 0
        for pkg in packages_in_route:
            total_mile += int(pkg.get('travel_distance'))
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

    @staticmethod
    def update_packages_status_en_route(truck):
        for pkg in truck:
            if pkg.get('pid') == 0:
                pkg.update({'status': 'hub location place holder'})
                continue
            pkg.update({'status': 'en route'})

    def delivery_packages(self):
        start_time = Utils.start_time

        # Delivery pkgs in truck1
        Utils.update_packages_status_en_route(self.truck.truck1)
        self.delivery_pkgs_in_truck1(start_time)

        # Delivery pkgs in truck2
        Utils.update_packages_status_en_route(self.truck.truck2)
        self.delivery_pkgs_in_truck2(start_time)

        # Delivery pkgs in truck3
        Utils.update_packages_status_en_route(self.truck.truck3)
        start_time = self.get_start_time_based_on_early_return_driver()
        Utils.hub.update({'start_time': start_time})
        Utils.hub.update({'travel_distance': 0})

        self.delivery_pkgs_in_truck3(start_time)

    def delivery_pkgs_in_truck3(self, start_time):
        if start_time.time() >= Utils.format_time('10:20:00'):
            self.update_pkg9_address()
            hub_location = copy.deepcopy(Utils.hub)
            hub_location.update({'start_time:': start_time})

            route = self.find_fast_route(hub_location, self.truck.truck3)
            self.truck.truck3.clear()
            self.truck.truck3.extend(route)

            self.truck3_delivery(self.truck.truck3, start_time)
        else:
            route = self.get_route_without_pkg9(start_time)
            # Re-organize the packages in truck
            self.truck.truck3.clear()
            self.truck.truck3.extend(route)

            for i, pkg in enumerate(self.truck.truck3):
                # Check is package9's address has updated
                if start_time.time() >= Utils.format_time('10:20:00'):
                    self.update_pkg9_address()
                    self.add_pkg9_in_route_and_deliver(i, start_time)
                    break

                time_used, distance = Utils.update_pkg_delivery_info(pkg, start_time)
                start_time = pkg.get('delivery_time')

                # calculate total time used in minutes
                self.truck.total_delivery_time_truck3 += time_used
                # calculate total distance used in miles
                self.truck.total_delivery_miles_truck3 += distance

    def add_pkg9_in_route_and_deliver(self, index, st):
        for pkg in self.pkgs.package_with_wrong_address:
            self.truck.truck3.insert(index+1, pkg)
        new_route = self.find_fast_route(self.truck.truck3[index], self.truck.truck3[index+1:len(self.truck.truck3)-1])

        self.truck.truck3[index:len(self.truck.truck3)-1] = new_route

        self.append_hub_as_final_destination(self.truck.truck3)

        start_time = self.truck.truck3[index-1].get('delivery_time')
        if start_time == '':
            start_time = st
        self.truck3_delivery(self.truck.truck3[index + 1:], start_time)

    def truck3_delivery(self, truck, start_time):
        self.append_hub_as_final_destination(self.truck.truck3)
        for pkg in truck:
            time_used, distance = Utils.update_pkg_delivery_info(pkg, start_time)
            start_time = pkg.get('delivery_time')

            # calculate total time used in minutes
            self.truck.total_delivery_time_truck3 += time_used
            # calculate total distance used in miles
            self.truck.total_delivery_miles_truck3 += distance

    def get_start_time_based_on_early_return_driver(self):
        if self.truck.truck1[-1].get('delivery_time') > self.truck.truck2[-1].get('delivery_time'):
            return self.truck.truck2[-1].get('delivery_time')
        else:
            return self.truck.truck1[-1].get('delivery_time')

    def get_route_without_pkg9(self, start_time):
        self.truck.truck3.remove(self.pkgs.package_with_wrong_address[0])
        route = self.find_fast_route(Utils.hub, self.truck.truck3)
        return route

    def update_pkg9_address(self):
        self.pkgs.package_with_wrong_address[0].update({'address': '410 S State St'})
        self.pkgs.package_with_wrong_address[0].update({'city': 'Salt Lake City'})
        self.pkgs.package_with_wrong_address[0].update({'state': 'UT'})
        self.pkgs.package_with_wrong_address[0].update({'zip_code': '84111'})

    def delivery_pkgs_in_truck1(self, start_time):
        self.append_hub_as_final_destination(self.truck.truck1)
        for pkg in self.truck.truck1:
            time_used, distance = Utils.update_pkg_delivery_info(pkg, start_time)
            start_time = pkg.get('delivery_time')

            # calculate total time used in minutes
            self.truck.total_delivery_time_truck1 += time_used
            # calculate total distance used in miles
            self.truck.total_delivery_miles_truck1 += distance

    def delivery_pkgs_in_truck2(self, start_time):
        time_object = Utils.format_time('09:05:00')
        temp_id = -1
        for i, pkg in enumerate(self.truck.truck2):
            if pkg.get('pid') == 0 and i == temp_id:
                # Load to cargo and recalculate the route based on urgent delivery and then deliver the rest of packages
                index = self.load_urgent_delayed_packages(i)
                self.load_delayed_not_urgent_packages(index)
                self.recalculate_route_and_deliver(index-1, i)
                break

            time_used, distance = Utils.update_pkg_delivery_info(pkg, start_time)
            start_time = pkg.get('delivery_time')

            # calculate total time used in minutes
            self.truck.total_delivery_time_truck2 += time_used
            # calculate total distance used in miles
            self.truck.total_delivery_miles_truck2 += distance

            # Return to Hub to load the rest of delayed packages
            if pkg.get('delivery_time').time() >= time_object:
                current_address = pkg.get('address') + ' ' + pkg.get('zip_code')

                # next stop would be at the Hub for picking up delayed packages
                hub_location = copy.deepcopy(Utils.hub)
                self.truck.truck2.insert(i + 1, hub_location)
                temp_id = i + 1

                # Update the travel info from current location back to Hub
                self.update_inf_travel_back_to_hub(current_address, i, start_time)

    @staticmethod
    def format_time(start_time):
        time_return_hub_for_delayed_pkgs = start_time
        time_object = datetime.strptime(time_return_hub_for_delayed_pkgs, "%H:%M:%S").time()
        return time_object

    def update_inf_travel_back_to_hub(self, current_address, i, start_time):
        travel_distance = float(self.drive_back_hub(current_address))
        minutes_used_to_travel, new_time = Utils.calc_time(travel_distance, start_time)
        self.truck.truck2[i + 1].update({'travel_distance': travel_distance})
        self.truck.truck2[i + 1].update({'start_time': start_time})
        self.truck.truck2[i + 1].update({'delivery_time': new_time})

        # Update total delivery time and miles for truck2
        self.truck.total_delivery_time_truck2 += minutes_used_to_travel
        self.truck.total_delivery_miles_truck2 += travel_distance

    def recalculate_route_and_deliver(self, index, i):
        route = self.find_fast_route(self.truck.truck2[index], self.truck.truck2[index:])
        start_time = self.truck.truck2[i].get('delivery_time')

        self.truck.truck2[index + 1:] = route

        # Add hub as the last location - back to Hub at the EOD
        self.append_hub_as_final_destination(self.truck.truck2)

        # Start to deliver
        for pkg in self.truck.truck2[i:]:
            Utils.update_pkg_delivery_info(pkg, start_time)
            start_time = pkg.get('delivery_time')

    def load_urgent_delayed_packages(self, index):
        i = index
        route = self.find_fast_route(Utils.hub, self.pkgs.package_urgent_delayed_list)

        for count, pkg in enumerate(route):
            if len(self.truck.truck2[index:]) < 16:
                self.truck.truck2.insert(count + index + 1, pkg)
                i += 1
            else:
                print(
                    "You may need hire more drivers as truck1 and truck2 don't have capacity to carry delayed but urgent packages")
        return i

    def load_delayed_not_urgent_packages(self, index):
        for pkg in self.pkgs.package_not_urgent_delayed_list:
            if len(self.truck.truck2[index:]) < 16:
                self.truck.truck2.append(pkg)
            else:
                print(
                    "You may need hire more drivers as truck1 and truck2 don't have capacity to carry delayed but urgent packages")

    def drive_back_hub(self, current_address):
        hub_location_address = Utils.hub.get('address') + ' ' + Utils.hub.get('zip_code')
        return self.calc_distance(current_address, hub_location_address)

    @staticmethod
    def update_pkg_delivery_info(pkg, start_time):
        distance = float(pkg.get('travel_distance'))

        time_used, new_time = Utils.calc_time(distance, start_time)
        pkg.update({'start_time': start_time})
        pkg.update({'delivery_time': new_time})
        pkg.update({'status': 'delivered'})

        return time_used, distance

    @staticmethod
    def calc_time(dist, start_time):
        minutes_used_in_travel = float(
            dist * 60 / 18)  # total time in minutes used from current location to nearst location
        hours_to_add, remaining_minutes = divmod(minutes_used_in_travel, 60)
        time_delta = timedelta(hours=hours_to_add, minutes=remaining_minutes)

        new_time = datetime.combine(datetime.today(), start_time.time()) + time_delta
        return minutes_used_in_travel, new_time

