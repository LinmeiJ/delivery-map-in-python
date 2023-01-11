import copy
import time
from datetime import time, datetime

from Package import Package
from graph import Graph
from truck import Truck

# Load packages from a csv file
pkgs = Package(0, '', '', '', '', '', '', '', '', '', '', False)  # Create an instance of Package
pkgs.load_package_data()
# Load graph data from a csv file
graph = Graph()
# set hub location with a package placeholder
start_location = vars(Package(0, '4001 South 700 East',
                              'Salt Lake City', 'UT', '84107', '', '', '', '08:00 AM', '', 0, 'delivered'))

total_delivery_time_truck1 = 0
total_delivery_miles_truck1 = 0

total_delivery_time_truck2 = 0
total_delivery_miles_truck2 = 0

total_delivery_time_truck3 = 0
total_delivery_miles_truck3 = 0


def calc_distance(route1, route2):
    for kv in graph.address_with_distance.items():
        if kv[0] == route2:
            for elem in kv[1]:
                if elem[0] == route1:
                    return elem[1]


# TSP algorithm for planning a route for a fast delivery

def find_fast_route(sta_location, loaded_truck):
    pkg_in_truck = copy.deepcopy(loaded_truck)
    # Initialize a route
    route = [sta_location]

    # Keep looping until all locations have been visited
    while pkg_in_truck:
        # Find the nearest unvisited location to the current location
        nearest_location = None
        nearest_distance = float('inf')
        current_location = sta_location.get('address') + ' ' + sta_location.get('zip_code')
        for pkg in pkg_in_truck:
            nearest_address = pkg['address'] + ' ' + pkg['zip_code']
            location_distance = calc_distance(current_location,
                                              nearest_address)
            if location_distance != '' and location_distance is not None:
                dist = float(location_distance)
                if dist < nearest_distance:
                    nearest_location = pkg
                    nearest_distance = dist
        if nearest_location is not None:
            nearest_location.update({'travel_distance': nearest_distance})
            route.append(nearest_location)

            # Remove the nearest location from the list of unvisited locations
            pkg_in_truck.remove(
                nearest_location)
        # Set the current location to the nearest location
        current_location = nearest_location
    return route


def calc_time(dist):
    time_used = int(dist * 60 / 18)  # total time in minutes used from current location to nearst location
    travel_in_hour = int(time_used / 60)  # convert to hour if time_used more than or equal 60 minutes
    if travel_in_hour != 0:
        travel_in_minute = int(time_used % 60)  # get the remaining minutes if time travel is over an hour
    else:
        travel_in_minute = time_used  # less than 60 minutes
    return time_used, travel_in_hour, travel_in_minute


def format_time(dist, start_time):
    format_str = '%I:%M %p'
    time_obj = datetime.strptime(start_time, format_str).time()
    hour = time_obj.hour
    minute = time_obj.minute

    time_used, travel_in_hour, travel_in_minute = calc_time(dist)

    update_hour = hour + travel_in_hour
    update_minute = minute + travel_in_minute
    if update_minute > 59:
        update_hour += int(update_minute / 60)
        update_minute %= 60
    new_time = time(update_hour, update_minute, 0)

    return time_used, new_time.strftime('%I:%M %p')


def minute_per_mile():
    return 60 / 18


def calc_total_time_for_delivery(packages_in_truck):
    total_mile = 0
    for pkg in packages_in_truck:
        total_mile += pkg.get('travel_distance')
    total_time = minute_per_mile() * total_mile
    return int(total_time)


def can_delivery_on_time_for_all_pkg(estimate_time):
    if estimate_time > (60 * 2 + 30):  # start from 8AM to 10:30AM in minutes
        return False
    else:
        return True


def start_package_delivery(packages_in_route, total_time, total_miles, time_start_to_deliver):
    for pkg in packages_in_route:
        dist = pkg.get('travel_distance')
        time_used, delivered_time = format_time(dist, time_start_to_deliver)
        pkg.update({'start_time': delivered_time})
        pkg.update({'delivery_time': delivered_time})
        pkg.update({'status': 'delivered'})
        time_start_to_deliver = delivered_time
        total_time += time_used
        total_miles = round(total_time + dist)
    return total_time, total_miles, packages_in_route


def get_prioritize_route(s_location, trk):
    urgent_pkgs = []
    remaining_pkgs = []
    for pkg in trk:
        if pkg.get('deadline') != 'EOD':
            urgent_pkgs.append(pkg)
        else:
            remaining_pkgs.append(pkg)
    priority_pkgs_route = find_fast_route(s_location, urgent_pkgs)

    return priority_pkgs_route, remaining_pkgs


def plan_and_deliver_packages(trk):
    route_for_truck = find_fast_route(start_location, trk)
    route_for_truck.remove(start_location)  # remove the placeholder location from the list
    estimate_total_delivery_time = calc_total_time_for_delivery(route_for_truck)
    # if all packages can be delivered before or at 10:30AM
    if can_delivery_on_time_for_all_pkg(estimate_total_delivery_time) is True:
        route = start_package_delivery(route_for_truck, 0, 0, '8:00 AM')
    else:  # get a new route based on priority packages
        urgent_pkg_route_truck, remaining_pkg_truck = get_prioritize_route(start_location, trk)
        estimate_total_delivery_time = calc_total_time_for_delivery(urgent_pkg_route_truck)
        if can_delivery_on_time_for_all_pkg(estimate_total_delivery_time) is True:
            start_delivery_time = "08:00 AM"
            total_time, total_mile, route = start_package_delivery(urgent_pkg_route_truck, 0, 0, start_delivery_time)
            last_package_in_priority_route = urgent_pkg_route_truck[-1]
            start_delivery_time = last_package_in_priority_route.get('delivery_time')
            remaining_pkg_route = find_fast_route(last_package_in_priority_route, remaining_pkg_truck)
            total_time, total_mile, second_route = start_package_delivery(remaining_pkg_route, total_time, total_mile,
                                                                          start_delivery_time)
            route.extend(second_route)
        else:
            print(" Some packages may delayed")

    return total_time, total_mile, route


truck = Truck(pkgs.package_urgent_list, pkgs.package_urgent_delayed_list,
              pkgs.package_not_urgent_delayed_list, pkgs.package_with_wrong_address, pkgs.package_with_truck2_only,
              pkgs.package_must_on_same_truck,
              pkgs.package_remaining_packages)
truck.load_cargo()

# truck.truck1
truck1_total_time, truck1_total_mile, route_truck1 = plan_and_deliver_packages(truck.truck1)

truck2_total_time, truck2_total_mile, route_truck2 = plan_and_deliver_packages(truck.truck2)

truck3_total_time, truck3_total_mile, route_truck3 = plan_and_deliver_packages(truck.truck3)

print(f'{truck1_total_time}, {truck1_total_mile}, {route_truck1}')
print(f'{truck2_total_time}, {truck2_total_mile}, {route_truck2}')
print(f'{truck3_total_time}, {truck3_total_mile}, {route_truck3}')

#
# def get_distance(route):
#     pass
#
#
# def start_delivery(route_for_truck, total_time, total_miles):
#     for route in route_for_truck1:
#         get_distance(route)
#
#
# start_delivery(route_for_truck1, total_delivery_time, total_delivery_miles)

# print('======== WGUPS Routing Program =======')
# ans = True
# while ans:
#     print("""
#     1. Lookup A Package By Package ID
#     2. List All Packages By Time
#     3. Total Mileage Traveled By All Trucks
#     4. Exit/Quit
#     """)
#
#     ans = int(input("What Would You Like To Do? "))
#     if ans == 1:
#         print("do something")  # fix me
#     elif ans == 2:
#         print("do something")  # fix me
#     elif ans == 3:
#         print("do something")  # fix me
#     elif ans == 4:
#         print("\n Goodbye!")
#         ans = None
#     else:
#         print("\n Not Valid Choice. Try again")
