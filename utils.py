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
    pkgs_by_id = []

    def __init__(self):
        # Load packages from a csv file
        self.route1 = None
        self.route2 = None
        self.route3 = None

        # Initialize the packages
        self.pkgs = Package(0, '', '', '', '', '', '', '', '', '', '', False)  # Create an instance of Package
        self.pkgs.load_package_data()

        # Initialize a graph data (addresses and distances)
        self.graph = graph.Graph()

        # Set a list of pkgs without key from the hash table
        self.list_of_pkgs = self.remove_keys_from_pkgs_table()

        # Start to load packages to different trucks based on project requirement - This project is not doing manual loading to each truck
        self.pkg_loading_optimization()

        # Start to delivery packages
        self.delivery_packages()

        # Store the result of delivery to a separated package list for later to access
        pkgs = self.truck.truck1[0:-1] + self.truck.truck2[0:-1] + self.truck.truck3[0:-1]
        # Sore the package list order by package ID
        self.pkgs_by_id.extend(sorted(pkgs, key=lambda x: x.get('pid')))  # sort packages by package ID

    # Time complexity: O(N^2) >> due to it is calling the find_fast_route function
    # Space complexity: O(N) >> a number of lists are created in this function and each one takes an O(N) space
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

        # Load truck3 (since there are only 40 packages, the truck3 won't exceed its capacity)
        self.truck.load_packages_to_truck3(self.pkgs.package_with_wrong_address)
        self.truck.load_packages_to_truck3(self.pkgs.package_remaining_packages)

        self.route3 = self.find_fast_route(Utils.hub,
                                           self.truck.truck3)

    # Time complexity: O(N) >> Although it is a nested for loop, but the runtime only depends on the outer loop
    # Space complexity: O(N) >> a new list pkg_info created and the size of it proportional to the number of packages the package_table.table
    def remove_keys_from_pkgs_table(self):
        pkg_info = []
        for pkgs in self.pkgs.package_table.table:
            for pkg in pkgs:
                pkg_info.append(vars(pkg[1]))
        return pkg_info

    # Time complexity: O(N^2) >> N is total number of packages (pkg1 + pkg2), but it is calling the find_fast_route function which results a O(N^2)
    # Space complexity: O(N) >> Total number of packages (pkg1 + pkg2)
    # Load cargo when trucks are not full, and return a fast route
    def load_more_packages(self, urgent_pkg_route, truck, pkgs1, pkgs2):
        remaining_pkg_list = []  # Initialize a temp list in case we need find fast route independently

        # Optional.... different type of pkgs
        if pkgs1 is not None:
            for pkg in pkgs1:
                if pkg.get('status') != 'en route':
                    truck.append(pkg)
                    pkg.update({'status': 'en route'})
                    remaining_pkg_list.append(pkg)
        for pkg in pkgs2:
            if pkg.get('status') != 'en route':
                if len(truck) < 16:
                    truck.append(pkg)
                    pkg.update({'status': 'en route'})
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

    # Space complexity: O(1) >> creates a single copy of the "Utils.hub"
    # Time complexity: O(1)
    # The final destination is the Hub location
    def append_hub_as_final_destination(self, route):
        hub_location = copy.deepcopy(Utils.hub)
        current_address = route[-1].get('address') + ' ' + route[-1].get('zip_code')
        travel_distance = self.drive_back_hub(current_address)
        hub_location.update({'travel_distance': travel_distance})
        route.append(hub_location)

    # Time complexity: O(N^2) >> calling find_fast_route function results such time complexity
    # Space complexity: O(N) >> a new list is created, the remaining_route
    # Get a route based on package list that need to be delivered by 10:30AM
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

    # Runtime complexity: O(N^2) >> there is nested for loop iterating over 2 lists of packages, the urgent_route and remaining_route leads to a quadratic runtime
    # Space complexity: O(N) >>  this function creates a list - pkg_ids with a max size of N, where N is the number of items in the remaining_route list
    # As a truck is going to deliver urgent packages (deadline is before or at 10:30 consider as urgent packages), then deliver the rest. however, the rest of packages could contain
    # address that is already among the urgent package list. So we can remove the same address then later to calculate a fast route for the none-urgent packages
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

    # Time complexity: O(N^2) >> nested loop inside this function
    # Space complexity: O(1)
    def update_packages_status_route(self, pkgs):
        for pkg in self.pkgs.package_urgent_list:
            for p in pkgs:
                if pkg.get('pid') == p.get('pid'):
                    pkg.update({'status': 'en route'})
                    break

        for pkg in self.pkgs.package_must_on_same_truck:
            for p in pkgs:
                if pkg.get('pid') == p.get('pid'):
                    pkg.update({'status': 'en route'})
                    break

    # Time complexity: O(N^2) >> calling find_fast_route function results such time complexity
    # Space complexity: O(N) >> a new list is created as an example
    def set_route2(self):
        route = self.find_fast_route(Utils.hub, self.truck.truck2)
        if Utils.can_delivery_on_time_for_all_pkg(
                Utils.calc_total_time_for_delivery(route)):
            self.route2 = route

            self.truck.truck2.clear()
            self.truck.truck2.extend(route)
        else:
            self.find_new_route()

    # Time complexity: O(N^2) >> the find_fast_route function call takes over the overall time complexity
    # Space complexity: O(N) >> 2 lists are created to hold N numbers of packages.
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

    # Finalize the route for truck1
    def get_route_by_full_load_truck1(self, route_for_urgent_pkgs):
        # Update packages status to loaded
        self.update_packages_status_route(route_for_urgent_pkgs)

        # Load more packages to truck1
        self.truck.load_packages_to_truck1(route_for_urgent_pkgs)

        # Truck's max capacity is 16
        if len(self.truck.truck1) == 16:
            self.route1 = route_for_urgent_pkgs

        elif len(self.truck.truck1) < 16:
            self.route1 = self.load_partial_truck_and_get_route(route_for_urgent_pkgs, self.truck.truck1,
                                                                None,
                                                                self.pkgs.package_remaining_packages)

    # Time complexity: O(n) >> where n is the max size of the packages that need to be split.
    # Space complexity: O(n) >> 2 new lists are created to store a combination of N size packages from package_must_on_same_truck and package_remaining_packages
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
            pkg.update({'status': 'en route'})

        if max_hold != 0:
            for pkg in self.pkgs.package_remaining_packages:
                if count < max_hold:
                    urgent_pkgs1.append(pkg)
                    pkg.update({'status': 'en route'})
                elif rest_count == 0:
                    break

                urgent_pkgs2.append(pkg)
                pkg.update({'status': 'en route'})
                count += 1
                rest_count -= 1
        return urgent_pkgs1, urgent_pkgs2

    # Time complexity: O(n^2) >> the fund_fast_route function makes the overall time complexity
    # Space complexity: 0(n) >> 2 new list created >> urgent_pkgs1 and urgent_packages2
    def set_route_by_splitting_urgent_packages(self, route_for_urgent_pkgs):
        # find out how many urgent packages can one truck carry based on the latest delivery deadline at 10:30 AM
        num_of_pkgs = Utils.deliverable_packages_count(route_for_urgent_pkgs, Utils.start_time)
        # Split the urgent packages, load truck1 first
        urgent_pkgs1, urgent_pkgs2 = self.split_packages(num_of_pkgs, len(route_for_urgent_pkgs))

        self.truck.load_packages_to_truck1(self.find_fast_route(Utils.hub, urgent_pkgs1))
        self.update_packages_status_route(urgent_pkgs1)

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
        self.update_packages_status_route(urgent_pkgs2)

    def load_partial_truck_and_get_route(self, route_for_urgent_pkgs, truck, pkgs1, pkgs2):
        # Load more packages until truck1 is full and also set the final route for truck1
        return self.load_more_packages(route_for_urgent_pkgs, truck, pkgs1, pkgs2)

    # This calculates how many packages a truck carries to delivery all urgent package on time based on urgent package list
    # It uses a recursion algorithm to count time start from 8AM and ends at 10:30AM
    # returns a max number of urgent packages that one truck can carry and can also deliver on time.
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

    # Time complexity: O(N^2) >> The while loop iterates until all packages are visited which takes O(N) time. Inside the while loop, the for loop iterates over the packages list until the nearest
    # unvisited location is found which is another O(N) time complexity.
    # Space complexity: O(N)  >> n number of packages in route, and also deepcopy has a space complexity of O(n)
    # Nearest neighbor/Dijkstra's algorithm for planning a route for a fast delivery route >> self-adjusting algorithm
    def find_fast_route(self, sta_location, p):
        packages = copy.deepcopy(p)

        # Initialize a route and nearest location
        route = []
        nearest_address = ''

        if sta_location.get('pid') == 0:
            sta_location.update({'distance': 0})

        current_location = sta_location.get('address') + ' ' + sta_location.get('zip_code')
        # Keep looping until all locations have been visited
        while packages:
            # Find the nearest unvisited location to the current location
            location_holder = None
            nearest_distance = float('inf')
            for pkg in packages:
                nearest_address = pkg['address'] + ' ' + pkg['zip_code']
                location_distance = self.calc_distance(current_location, nearest_address)
                if location_distance != '' and location_distance is not None:
                    dist = float(location_distance)
                    if dist < nearest_distance:
                        location_holder = pkg
                        nearest_distance = dist
            if location_holder is not None:
                if self.is_same_address(nearest_address, current_location):
                    location_holder.update({'travel_distance': 0})
                else:
                    location_holder.update({'travel_distance': nearest_distance})
                route.append(location_holder)

                # Remove the nearest location from the list of unvisited locations
                packages.remove(
                    location_holder)
                # Set the current location to the nearest location
                current_location = location_holder.get('address') + ' ' + location_holder.get('zip_code')
        return route

    # Runtime complexity: O(N) >> n is the number of key value pairs in the graph.
    # Space complexity: O(1)
    def calc_distance(self, start, end):
        for kv in self.graph.address_with_distance.items():
            if kv[0] == start:
                for elem in kv[1]:
                    if elem[0] == end:
                        return elem[1]

    @staticmethod
    def minute_per_mile():
        return float(60 / 18)

    # Time complexity: O(N)
    # Space complexity: O(1)
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

    # Time complexity: O(N) >> where n is the number of packages
    # Space complexity: 0(1)
    @staticmethod
    def update_packages_status_en_route(truck):
        for pkg in truck:
            if pkg.get('pid') == 0:
                pkg.update({'status': 'hub location place holder'})
                continue
            pkg.update({'status': 'en route'})

    # Time complexity: O(N) >> this function calls three different functions, each could have a max size of n, where n is the number of items in the list
    # Space complexity: O(1) >> no new data structures created inside this function
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
        Utils.hub.update({'start_time': ''})
        Utils.hub.update({'delivery_time': ''})
        Utils.hub.update({'travel_distance': 0})

        self.delivery_pkgs_in_truck3(start_time)

    # Time complexity: O(N^2) >> the fund_fast_route function makes the overall time complexity
    # Space complexity: O(N) >> due to the usage of deepcopy function that has created a new object - hub_location. Also,
    # the function calls Utils.format_time once and Utils.update_pkg_delivery_info n times but since the function has a linear complexity,
    # the complexity of the function is still O(N).
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
            route = self.get_route_without_pkg9()
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

    # Time complexity: O(N^2) >> the fund_fast_route function makes the overall time complexity
    # Space complexity: O(N)  >> the function uses the insert function to add packages to truck3, then uses the slice operator to extract a list from the truck3 and assign it to
    # a new list. Then slice the truck3 again for deleting the extracted items from truck3 list.
    def add_pkg9_in_route_and_deliver(self, index, st):
        for pkg in self.pkgs.package_with_wrong_address:
            self.truck.truck3.insert(index + 1, pkg)
        new_route = self.find_fast_route(self.truck.truck3[index],
                                         self.truck.truck3[index + 1:len(self.truck.truck3) - 1])

        self.truck.truck3[index:len(self.truck.truck3) - 1] = new_route

        self.append_hub_as_final_destination(self.truck.truck3)

        start_time = self.truck.truck3[index - 1].get('delivery_time')
        if start_time == '':
            start_time = st
        self.truck3_delivery(self.truck.truck3[index + 1:], start_time)

    # Time complexity: O(N) >> where n is the number of packages in the truck
    # Space complexity: O(1)
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

    # Time complexity: O(n^2) >> the fund_fast_route function makes the overall time complexity
    # Space complexity: O(n) >> the route list takes a O(n) space
    def get_route_without_pkg9(self):
        self.truck.truck3.remove(self.pkgs.package_with_wrong_address[0])
        route = self.find_fast_route(Utils.hub, self.truck.truck3)
        return route

    def update_pkg9_address(self):
        self.pkgs.package_with_wrong_address[0].update({'address': '410 S State St'})
        self.pkgs.package_with_wrong_address[0].update({'city': 'Salt Lake City'})
        self.pkgs.package_with_wrong_address[0].update({'state': 'UT'})
        self.pkgs.package_with_wrong_address[0].update({'zip_code': '84111'})

    # Time complexity: O(N) >> where n is the max size of pkgs in truck1
    # Space complexity: O(1)
    def delivery_pkgs_in_truck1(self, start_time):
        self.append_hub_as_final_destination(self.truck.truck1)
        for pkg in self.truck.truck1:
            time_used, distance = Utils.update_pkg_delivery_info(pkg, start_time)
            start_time = pkg.get('delivery_time')

            # calculate total time used in minutes
            self.truck.total_delivery_time_truck1 += time_used
            # calculate total distance used in miles
            self.truck.total_delivery_miles_truck1 += distance

    # Time complexity: O(N) >> where n is the max size of the packages in the truck2
    # Space complexity: O(N) >> due to deepcopy the Utils.hub created a new object and then uses an insert function to add the items of the new object to truck2 list
    def delivery_pkgs_in_truck2(self, start_time):
        time_object = Utils.format_time('08:55:00')
        temp_id = -1
        for i, pkg in enumerate(self.truck.truck2):
            if pkg.get('pid') == 0 and i == temp_id:
                # Load to cargo and recalculate the route based on urgent delivery and then deliver the rest of packages
                index = self.load_urgent_delayed_packages(i)
                self.load_delayed_not_urgent_packages(index)
                self.recalculate_route_and_deliver(index - 1, i)
                break

            time_used, distance = Utils.update_pkg_delivery_info(pkg, start_time)
            start_time = pkg.get('delivery_time')

            # calculate total time used in minutes
            self.truck.total_delivery_time_truck2 += time_used
            # calculate total distance used in miles
            self.truck.total_delivery_miles_truck2 += distance

            # Return to Hub to load the rest of delayed packages when it's close to the time flight arrives
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

    def update_inf_travel_back_to_hub(self, current_address, i, st_time):
        travel_distance = float(self.drive_back_hub(current_address))
        minutes_used_to_travel, new_time = Utils.calc_time(travel_distance, st_time)
        self.truck.truck2[i + 1].update({'travel_distance': travel_distance})
        self.truck.truck2[i + 1].update({'start_time': st_time})
        self.truck.truck2[i + 1].update({'delivery_time': new_time})

        # Update total delivery time and miles for truck2
        self.truck.total_delivery_time_truck2 += minutes_used_to_travel
        self.truck.total_delivery_miles_truck2 += travel_distance

    # Time complexity: O(N^2) >> the function call to find_fast_route takes overall time complexity
    # Space complexity: O(N) >> slice operator creates a new list object with the same elements which takes up additional memory.
    def recalculate_route_and_deliver(self, index, i):
        route = self.find_fast_route(self.truck.truck2[index], self.truck.truck2[index:])
        start_time = self.truck.truck2[i].get('delivery_time')

        self.truck.truck2[index:] = route

        # Add hub as the last location - back to Hub at the EOD
        self.append_hub_as_final_destination(self.truck.truck2)

        # Start to deliver
        for pkg in self.truck.truck2[i:]:
            Utils.update_pkg_delivery_info(pkg, start_time)
            start_time = pkg.get('delivery_time')

    # Time complexity: O(N^2) >> the function call to find_fast_route takes overall time complexity
    # Space complexity: 0(N) >> insertion function is used to add items from the route to truck2. where n is the max size of packages in route.
    def load_urgent_delayed_packages(self, index):
        i = index
        route = self.find_fast_route(Utils.hub, self.pkgs.package_urgent_delayed_list)

        for count, pkg in enumerate(route):
            if len(self.truck.truck2[index + 1:]) < 16:
                self.truck.truck2.insert(count + index + 1, pkg)
                i += 1
            else:
                print(
                    "You may need hire more drivers as truck1 and truck2 don't have capacity to carry delayed but urgent packages")
        return i

    # Time complexity: O(N) >> where the n is the max size of packages in package_not_urgent_delayed_list
    # Space complexity: O(N) >> due to each element in the not urgent package delayed list will be added to truck2. the size of truck2 increases based on the size of packages in the delayed list.
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

    def display_all_trucks_traveled_by_time(self):
        total_miles = math.ceil(
            self.truck.total_delivery_miles_truck1 + self.truck.total_delivery_miles_truck2 + self.truck.total_delivery_miles_truck3)
        print(
            '===========================================================================================================================================================')
        print(
            f'The total distance covered by all trucks is:  {total_miles} miles  (including the return trips from the last package delivery to the hub for three trucks)')
        print(
            '===========================================================================================================================================================')

    # Time Complexity: O(log n) >> as the pkgs_by_id is in order with package ID, the binary search algorithm cuts the search space in half on each iteration.
    # Space Complexity: O(1)
    @staticmethod
    def binary_search(pid):
        low = 0
        high = len(Utils.pkgs_by_id[1:])  # Exclude the starting index which is just a place hold for the Hub location

        while low <= high:
            mid = (high + low) // 2
            if Utils.pkgs_by_id[mid].get('pid') < pid:
                low = mid + 1
            elif Utils.pkgs_by_id[mid].get('pid') > pid:
                high = mid - 1
            else:
                return Utils.pkgs_by_id[mid]
        return -1

    @staticmethod
    def display_package_by_pkg_id(pid, time):
        pkg = Utils.binary_search(pid)
        start_time = '08:00:00'
        # Utils.packages_status_time_range


        print(
            '========================================================================================================================================================')
        header = ['Package ID Number', 'Delivery Address', 'Delivery City', 'Delivery Zip Code', 'Delivery Deadline',
                  'Package Weight', 'delivery_time', 'Delivery Status']
        print('{:<25s} {:<25s} {:<25s} {:<25s} {:<25s} {:<25s} {:<25s} {:<25s}'.format(*header))
        Utils.table_format(pkg)
        print(
            '========================================================================================================================================================')

    @staticmethod
    def table_format(pkg):
        print('{:<1s} {:<15d} {:<25s} {:<20s} {:<25s} {:<25s} {:<15s} {:<25s} {:<25s}'.format('', pkg.get('pid'),
                                                                                              pkg.get('address'),
                                                                                              pkg.get('city'),
                                                                                              pkg.get('zip_code'),
                                                                                              pkg.get('deadline'),
                                                                                              pkg.get('weight'),
                                                                                              Utils.format_time_column(
                                                                                                  pkg),
                                                                                              pkg.get('status')))

    @staticmethod
    def format_time_column(pkg):
        if pkg.get('delivery_time') != '':
            return str(pkg.get('delivery_time').time())
        else:
            return ''

    @staticmethod
    def revert_pkg_status_en_route(pkg):
        pkg.update({'start_time': ''})
        pkg.update({'delivery_time': ''})
        pkg.update({'status': 'en route'})

    @staticmethod
    def revert_pkg_status_at_hub(pkg):
        pkg.update({'start_time': ''})
        pkg.update({'delivery_time': ''})
        pkg.update({'status': 'at the Hub'})

    # Time complexity: O(nlogn) >> The function uses sorted() function which is TimeSort, a combination of insertion sort and merge sort
    # Space complexity: O(n) >> a list of all_pkgs_time_range is created in the function
    def display_packages_by_time(self, end_time):
        start_time = '08:00:00'
        all_pkgs_time_range = []

        self.packages_status_time_range(start_time, end_time, all_pkgs_time_range)

        all_pkgs_time_range = sorted(all_pkgs_time_range, key=lambda x: x.get('pid'))  # sort packages by package ID
        # all_pkgs_time_range = sorted(all_pkgs_time_range, key=lambda x: x.get('pid'))  # sort packages by package ID

        print(
            '====================================================================================================================================================================================')
        header = ['Package ID Number', 'Delivery Address', 'Delivery City', 'Delivery Zip Code', 'Delivery Deadline',
                  'Package Weight', 'delivery_time', 'Delivery Status']
        print('{:<20s} {:<20s} {:<15s} {:<25s} {:<25s} {:<20s} {:<25s} {:<25s}'.format(*header))
        print(
            '====================================================================================================================================================================================')

        for pkg in all_pkgs_time_range:
            if pkg.get('pid') == 0:
                continue
            Utils.table_format(pkg)
        print(
            '====================================================================================================================================================================================')

    # Time complexity: O(n) >> where n is the total number of packages in the truck1, truck2, and truck3 with a linear search through each package in those 3 truck lists
    # Space complexity:
    def packages_status_time_range(self, start, end, all_pkgs):
        truck1 = copy.deepcopy(self.truck.truck1)
        truck2 = copy.deepcopy(self.truck.truck2)
        truck3 = copy.deepcopy(self.truck.truck3)
        self.update_status_based_on_time(all_pkgs, truck1, truck2, truck3, start, end)

    # Time complexity: O(n) >> where n is the max size of numbers of packages in trucks >> 3 iteration is actually a O(3n) but it is the same as O(n)
    # Space complexity: 0(n) >> due to all 3 trucks will be added to the all_pkgs list in worst case scenario
    def update_status_based_on_time(self, all_pkgs, truck1, truck2, truck3, start, end):
        for pkg in truck1:
            if pkg.get('delivery_time').time() >= Utils.format_time(start) and pkg.get(
                    'delivery_time').time() <= Utils.format_time(end):
                all_pkgs.append(pkg)
            else:
                Utils.revert_pkg_status_en_route(pkg)
                all_pkgs.append(pkg)

        for pkg in truck2:
            if pkg.get('delivery_time').time() >= Utils.format_time(start) and pkg.get(
                    'delivery_time').time() <= Utils.format_time(end):
                all_pkgs.append(pkg)
            else:
                Utils.revert_pkg_status_en_route(pkg)
                all_pkgs.append(pkg)

        for pkg in truck3:
            if pkg.get('pid') == 0:
                continue
            if self.truck.truck3[0].get("start_time").time() > Utils.format_time(end):
                Utils.revert_pkg_status_at_hub(pkg)
                all_pkgs.append(pkg)
            elif pkg.get('delivery_time').time() <= Utils.format_time(end):
                all_pkgs.append(pkg)
            else:
                Utils.revert_pkg_status_en_route(pkg)
                all_pkgs.append(pkg)
