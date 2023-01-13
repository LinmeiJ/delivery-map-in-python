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
hub = vars(Package(0, '4001 South 700 East',
                   'Salt Lake City', 'UT', '84107', '', '', '', '08:00 AM', '', 0, 'delivered'))

total_delivery_time_truck1 = 0
total_delivery_miles_truck1 = 0

total_delivery_time_truck2 = 0
total_delivery_miles_truck2 = 0

total_delivery_time_truck3 = 0
total_delivery_miles_truck3 = 0


def calc_distance(address1, address2):
    for kv in graph.address_with_distance.items():
        if kv[0] == address1:
            for elem in kv[1]:
                if elem[0] == address2:
                    return elem[1]


# TSP algorithm for planning a route for a fast delivery

def find_fast_route(sta_location, loaded_truck):
    pkg_in_truck = copy.deepcopy(loaded_truck)
    # Initialize a route
    route = [sta_location]
    current_location = sta_location.get('address') + ' ' + sta_location.get('zip_code')

    # Keep looping until all locations have been visited
    while pkg_in_truck:
        # Find the nearest unvisited location to the current location
        nearest_location = None
        nearest_distance = float('inf')
        for pkg in pkg_in_truck:
            # if pkg['status'] == 'delivered':
            nearest_address = pkg['address'] + ' ' + pkg['zip_code']
            location_distance = calc_distance(current_location,
                                              nearest_address)
            if location_distance != '' and location_distance is not None:
                dist = float(location_distance)
                if dist < nearest_distance:
                    nearest_location = pkg
                    nearest_distance = dist
        if nearest_location is not None:
            if is_same_address(nearest_address, current_location):
                nearest_location.update({'travel_distance': 0})
            else:
                nearest_location.update({'travel_distance': nearest_distance})
            route.append(nearest_location)

            # Remove the nearest location from the list of unvisited locations
            pkg_in_truck.remove(
                nearest_location)
            # Set the current location to the nearest location
            current_location = nearest_location.get('address') + ' ' + nearest_location.get('zip_code')
    return route


def is_same_address(pkg_address, current_location):
    if current_location == pkg_address:
        return True
    else:
        return False


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
    return float(60 / 18)


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


def start_package_delivery(packages_in_route, total_time, total_miles, time_start_to_deliver, hub_location, pkg9=None):

    packages_in_route.append(hub_location)

    # Calculate the time back to Hub after delivered all packages
    last_package_location = packages_in_route[-2].get('address') + ' ' + packages_in_route[-2].get('zip_code')
    hub_address = packages_in_route[-1].get('address') + ' ' + packages_in_route[-1].get('zip_code')
    distance_to_hub = float(calc_distance(hub_address, last_package_location))
    start_loc = None
    for pkg in packages_in_route:
        dist = pkg.get('travel_distance')
        time_used, delivered_time = format_time(dist, time_start_to_deliver)
        pkg.update({'start_time': delivered_time})
        pkg.update({'delivery_time': delivered_time})
        pkg.update({'status': 'delivered'})
        time_start_to_deliver = delivered_time
        total_time += time_used
        total_miles += dist
        start_loc = pkg
        if pkg9 is not None and is_address_updated(pkg.get('delivery_time')):
            packages_in_route.append(pkg9)
            new_route = find_fast_route(start_loc, packages_in_route)
            total_time, total_miles, route = start_package_delivery(new_route, total_time, total_miles, start_loc.get('delivery_time'), hub_location)
            break
    total_miles += round(distance_to_hub, 2)

    total_time = total_time + int(distance_to_hub * minute_per_mile())

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


def is_address_updated(leaving_hub_time):
    format_str = '%I:%M %p'
    time_obj = datetime.strptime(leaving_hub_time, format_str).time()
    hour = time_obj.hour
    minute = time_obj.minute
    # Package #9 >>> wrong address and its address will be updated at 10:20AM
    if hour > 10:
        return True
    elif hour == 10:
        if minute >= 20:
            return True
        else:
            return False
    else:
        return False


def remove_package(packages_truck3):
    for pkg in packages_truck3:
        if pkg.get('pid') == 9:
            packages_truck3.remove(pkg)
            break
    return pkg


def plan_and_deliver_packages(trk, truck_number, leaving_hub_time):
    total_time = 0
    total_mile = 0
    route = []
    pkg9 = None
    route_for_truck = find_fast_route(hub, trk)
    if truck_number == 'truck3':
        for p in route_for_truck:
            if p.get('pid') == 9:
                route_for_truck.remove(p)
                route_for_truck.remove(hub)
                pkg9 = p
        route_for_truck = find_fast_route(hub, route_for_truck)
    route_for_truck.remove(hub)  # remove the placeholder location from the list
    estimate_total_delivery_time = 0

    # truck 1 contains many packages that need an urgent delivery, we need make sure they are delivered on time.
    # if the first route plan doesn't work, we need to prioritize the delivery route.
    if truck_number == 'truck1':
        estimate_total_delivery_time = calc_total_time_for_delivery(route_for_truck)
    # if all packages can be delivered before or at 10:30AM
    if can_delivery_on_time_for_all_pkg(estimate_total_delivery_time) is True:
        total_time, total_mile, route = start_package_delivery(route_for_truck, 0, 0, leaving_hub_time, hub, pkg9)
    else:  # get a new route based on priority packages
        urgent_pkg_route_truck, remaining_pkg_truck = get_prioritize_route(hub, trk)
        estimate_total_delivery_time = calc_total_time_for_delivery(urgent_pkg_route_truck)
        if can_delivery_on_time_for_all_pkg(estimate_total_delivery_time) is True:
            total_time, total_mile, route = start_package_delivery(urgent_pkg_route_truck, 0, 0, leaving_hub_time, hub)
            last_package_in_priority_route = urgent_pkg_route_truck[-1]
            leaving_hub_time = last_package_in_priority_route.get('delivery_time')
            remaining_pkg_route = find_fast_route(last_package_in_priority_route, remaining_pkg_truck)
            total_time, total_mile, second_route = start_package_delivery(remaining_pkg_route, total_time, total_mile,
                                                                          leaving_hub_time, hub)
            route.extend(second_route)
        else:
            print('You may need hire more drivers as some of the packages might not able to make on time')
    return total_time, total_mile, route


truck = Truck(pkgs.package_urgent_list, pkgs.package_urgent_delayed_list,
              pkgs.package_not_urgent_delayed_list, pkgs.package_with_wrong_address, pkgs.package_with_truck2_only,
              pkgs.package_must_on_same_truck,
              pkgs.package_remaining_packages)
truck.load_cargo()

# despite package id 15 requires delivery at 9:00AM, based on the current route, it will deliver on time
truck1_total_time, truck1_total_mile, route1 = plan_and_deliver_packages(truck.truck1, "truck1", '08:00 AM')  # driver1
truck2_total_time, truck2_total_mile, route2 = plan_and_deliver_packages(truck.truck2, "truck2", '09:05 AM')  # driver2
start_delivery_time = route1[-1].get('delivery_time')
truck3_total_time, truck3_total_mile, route3 = plan_and_deliver_packages(truck.truck3, "truck3",
                                                                         start_delivery_time)  # diver1

# truck2_total_time, truck2_total_mile, route_truck2 = plan_and_deliver_packages(truck.truck2)

# truck3_total_time, truck3_total_mile, route_truck3 = plan_and_deliver_packages(truck.truck3)

print(f'{truck1_total_time}, {truck1_total_mile}')
print(f'{truck2_total_time}, {truck2_total_mile}')
print(f'{truck3_total_time}, {truck3_total_mile}')

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
