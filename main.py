from Package import Package
from graph import Graph
from truck import Truck

# Load packages from a csv file
pkgs = Package(0, '', '', '', '', '', '', '', '', '', False)  # Create an instance of Package
pkgs.load_package_data()
# Load graph data from a csv file
graph = Graph()

# set hub location with a package placeholder
start_location = vars(Package(0, '4001 South 700 East', '', '', '84107', '', '', '', '', '', 'delivered'))


def calc_distance(route1, route2):
    for kv in graph.address_with_distance.items():
        if kv[0] == route2:
            for elem in kv[1]:
                if elem[0] == route1:
                    return elem[1]


# TSP algorithm for planning a route for a fast delivery
def find_fastest_route(sta_location, loaded_truck, sta_time):
    # Initialize a route and assign current location to it
    route = []
    priority_pkgs = []
    current_time = start_time
    for pkg in loaded_truck:
        if pkg.get('deadline') != 'EOD':
            priority_pkgs.append(pkg)
    # Plan a route for priority packages first
    add_nearest_locations_to_route(priority_pkgs, route, sta_location, current_time)
    # plan the route based on existing priory route
    add_nearest_locations_to_route(loaded_truck, route, sta_location, current_time)

    # Return the final route
    return route


def add_nearest_locations_to_route(loaded_truck, route, sta_location, sta_time):
    # Keep looping until all locations have been visited
    route.append(start_location)
    while loaded_truck:
        # Find the nearest unvisited location to the current location
        nearest_location = None
        nearest_distance = float('inf')
        for pkg in route:
            current_location = pkg.get('address') + ' ' + pkg.get('zip_code')

        for pkg in loaded_truck:
            if route.count(pkg) > 0:
                continue
            else:
                address = pkg.get('address') + ' ' + pkg.get('zip_code')
                location_distance = calc_distance(current_location, address)
                if location_distance != '' and location_distance is not None:
                    dist = float(location_distance)
                    if dist < nearest_distance:
                        nearest_location = pkg
                        nearest_distance = dist
        if nearest_location is not None:
            # calc_delivery_time_by_distance(route, nearest_distance, start_time)  # fix me -->  need to calculate the time and delivery status, 
            # Add the nearest location to the route
            route.append(nearest_location)
            # Remove the nearest location from the list of unvisited locations
            loaded_truck.remove(
                nearest_location)
        # Set the current location to the nearest location
        current_location = nearest_location


# fast_route_plan_for_all_packages = find_fastest_route(start_location, pkgs.all_package_info_list)
# fast_route_plan_for_all_packages.remove(start_location)  # remove the placeholder location from the list
# print(fast_route_plan_for_all_packages)


truck = Truck(pkgs.package_urgent_list, pkgs.package_urgent_delayed_list,
              pkgs.package_not_urgent_delayed_list, pkgs.package_with_wrong_address, pkgs.package_with_truck2_only,
              pkgs.package_must_on_same_truck,
              pkgs.package_remaining_packages)
truck.load_cargo()
start_time = "8:00 AM"
route_for_truck1 = find_fastest_route(start_location, truck.truck3, start_time)
route_for_truck1.remove(start_location)   # remove the placeholder location from the list
print(route_for_truck1)

#
# route_for_truck2 = find_fastest_route(start_location, truck.truck1)
# route_for_truck2.remove(start_location)   # remove the placeholder location from the list
# print(route_for_truck2)


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
