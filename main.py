from Package import Package
from graph import Graph
from truck import Truck

# Load packages from a csv file
pkgs = Package(0, '', '', '', '', '', '', '', '', '', False)  # Create an instance of Package
pkgs.load_package_data()
# Load graph data from a csv file
graph = Graph()
# Initialize a truck object
truck = Truck(pkgs.package_table)

# set hub location
start_location = '4001 South 700 East 84107'

def calc_distance(route1, route2):
    for kv in graph.address_with_distance.items():
        if kv[0] == route2:
            for elem in kv[1]:
                if elem[0] == route1:
                    return elem[1]


# Fix me: this is just for finding the fastest route for truck1. it can be refactored and combined with other method
# / can be fixed when there is time
def get_address_from_truck(trk):
    locations = []

    # get a list of just address of all packages
    for pkg in trk:
        locations.append(pkg.get('address') + ' ' + pkg.get('zip_code'))

    return locations


# TSP algorithm for planning a route for a fast delivery
def find_fastest_route(current_location, locations):
    # Initialize a route and assign current location to it
    route = [current_location]

    # Keep looping until all locations have been visited
    while locations:
        # Find the nearest unvisited location to the current location
        nearest_location = None
        nearest_distance = float('inf')
        for location in locations:
            if type(location) is dict:
                address = location['address'] + ' ' + location['zip_code']
            else:
                address = vars(location[1]).get('address') + ' ' + vars(location[1]).get('zip_code')
            location_distance = calc_distance(current_location, address)
            if location_distance != '' and location_distance is not None:
                dist = float(location_distance)
                if dist < nearest_distance:
                    nearest_location = location
                    nearest_distance = dist

        if nearest_location is not None:
            # Add the nearest location to the route
            route.append(nearest_location)
            # Remove the nearest location from the list of unvisited locations
            locations.remove(nearest_location)

        # Set the current location to the nearest location
        current_location = nearest_location
        break
    # Return the final route
    return route

truck.load_cargo(pkgs)


route_plan_for_all_pkg = find_fastest_route(start_location, pkgs.all_package_info_list)
route_for_urgent_delivery = find_fastest_route(start_location, pkgs.package_urgent_list)
shortest_path_truck1 = find_fastest_route(start_location, get_address_from_truck(truck.truck1))

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
