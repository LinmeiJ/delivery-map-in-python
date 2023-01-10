import time
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

total_delivery_time = 0
total_delivery_miles = 0


def calc_distance(route1, route2):
    for kv in graph.address_with_distance.items():
        if kv[0] == route2:
            for elem in kv[1]:
                if elem[0] == route1:
                    return elem[1]


# TSP algorithm for planning a route for a fast delivery

def find_fast_route(sta_location, loaded_truck):
    # Initialize a route
    route = [sta_location]

    # Keep looping until all locations have been visited
    while loaded_truck:
        # Find the nearest unvisited location to the current location
        nearest_location = None
        nearest_distance = float('inf')
        current_location = sta_location.get('address') + ' ' + sta_location.get('zip_code')
        for pkg in loaded_truck:
            nearest_address = pkg.get('address') + ' ' + pkg.get('zip_code')
            location_distance = calc_distance(current_location, nearest_address)
            if location_distance != '' and location_distance is not None:
                dist = float(location_distance)
                if dist < nearest_distance:
                    nearest_location = pkg
                    nearest_distance = dist
        if nearest_location is not None:
            nearest_location.update({'travel_distance': nearest_distance})
            route.append(nearest_location)

            # Remove the nearest location from the list of unvisited locations
            loaded_truck.remove(
                nearest_location)
        # Set the current location to the nearest location
        current_location = nearest_location
    return route


def calc_time(dist):
    time_used = dist * 60 / 18  # total time in minutes used from current location to nearst location
    travel_in_hour = time_used / 60  # convert to hour if time_used more than or equal 60 minutes
    if travel_in_hour != 0:
        travel_in_minute = time_used % 60  # get the remaining minutes if time travel is over an hour
    else:
        travel_in_minute = time_used  # less than 60 minutes
    return time_used, travel_in_hour, travel_in_minute


def format_time(dist, start_time):
    format_codes = "%I:%M %p"
    time_obj = time.strptime(start_time, format_codes)
    hour = time_obj[3]
    minute = time_obj[4]

    time_used, travel_in_hour, travel_in_minute = calc_time(dist)

    update_hour = hour + travel_in_hour
    update_minute = minute + travel_in_minute

    if update_hour > 11:
        meridiem = 'PM'
    if update_hour > 12:
        update_hour = update_hour - 12

    new_time = f'{update_hour}:{update_minute} {meridiem}'

    return time_used, new_time


truck = Truck(pkgs.package_urgent_list, pkgs.package_urgent_delayed_list,
              pkgs.package_not_urgent_delayed_list, pkgs.package_with_wrong_address, pkgs.package_with_truck2_only,
              pkgs.package_must_on_same_truck,
              pkgs.package_remaining_packages)
truck.load_cargo()

route_for_truck1 = find_fast_route(start_location, truck.truck1)
route_for_truck1.remove(start_location)  # remove the placeholder location from the list
print(route_for_truck1)
#
def get_distance(route):
    pass


def start_delivery(route_for_truck, total_time, total_miles):
    for route in route_for_truck1:
        get_distance(route)


start_delivery(route_for_truck1, total_delivery_time, total_delivery_miles)

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
