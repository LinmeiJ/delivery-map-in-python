import service
import HashTable


# Initialize an empty hashtable to store packages
# Initialize an empty hashtable to store packages and empty dictionary to store addresses and distances
packageTable = HashTable.ChainingHashTable()
# Initialize an empty dictionary to store the vertexes and edges of the graph
graph = {}

# set hub location
start_location = '4001 South 700 East 84107'

# Load data from csv files
service.LoadData(packageTable, graph)
# print(packageTable.table)

# Initialize three empty trucks
truck1 = []
truck2 = []
truck3 = []

# Category packages for different usages
package_info_list = []
package_address_list = []
package_urgent_list = []

# Split packages and load into trucks. Each truck can carry a max of 16 packages
def load_cargo():
    for bucket in packageTable.table:
        for index, pkg in enumerate(bucket):
            if len(truck1) < 16:
                truck1.append(pkg)
            elif len(truck2) < 16:
                truck2.append(pkg)
            else:
                truck3.append(pkg)

def get_list_of_address():
    for pkgs in packageTable.table:
        for pkg in pkgs:
            package_address_list.append(vars(pkg[1]).get('address') + ' ' + vars(pkg[1]).get('zip_code'))

# load package into each truck
load_cargo()

def get_list_of_pkg_info():
    for pkgs in packageTable.table:
        for pkg in pkgs:
            package_info_list.append(vars(pkg[1]))

# find the distance between 2 locations
def calc_distance(route1, route2):
    graph_dict = dict(graph.get(route1))
    return graph_dict.get(route2)

get_list_of_address()
get_list_of_pkg_info()

def tsp_shortest_path(truck, start):
    # Create a list of the locations that have not been visited yet
    undelivered_pkg = truck.copy()

    # find the package that is already at the start location:  O(N)
    for i, pkg in enumerate(undelivered_pkg):
        pkg_id = pkg[0]
        pkg_address = vars(pkg[1]).get("address") + " " + vars(pkg[1]).get("zip_code")
        # unload the packages that are for current starting location and mark the status as delivered
        if start == pkg_address:
            packageTable.update_pkg_delivery_status(pkg_id, 'delivered')
            undelivered_pkg.remove(pkg)
# print(package_address_list)


# find the distance between 2 locations
def calc_distance(route1, route2):
    for kv in graph.items():  # one way to go around program through a TypeError if when access as graph.get(route2)
        if kv[0] == route2:
            for elem in kv[1]:
                if elem[0] == route1:
                    return elem[1];


def get_address_from_package_list(truck, start):
    # Set the current location to the starting location
    current_location = start
    # Initialize an empty route
    route = [current_location]

    locations = []
    # get a list of just address of all packages
    for pkg in truck:
        locations.append(vars(pkg[1]).get("address") + " " + vars(pkg[1]).get("zip_code"))
        locations.append(pkg.get('address') + ' ' + pkg.get('zip_code'))

    return find_fastest_route(current_location, locations)


    print(locations)
    print('+++')
# TSP algorithm
def find_fastest_route(current_location, locations):
    # Initialize an empty route
    route = [current_location]
    # Keep looping until all locations have been visited
    while locations:
        # Find the nearest unvisited location to the current location
@ -70,28 +73,82 @@ def tsp_shortest_path(truck, start):
        nearest_distance = float('inf')
        for location in locations:
            location_distance = calc_distance(current_location, location)
            if location_distance != '':
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

    # Return the final route
    return route


start_location = "4001 South 700 East 84107"
print(tsp_shortest_path(truck1, start_location))
# shortest_route_for_truck1 = tsp_shortest_path(truck1, start_location)
route_plan_for_all_pkg = find_fastest_route(start_location, package_address_list)
# print(route_plan_for_all_pkg)


# Deadline: 1) pkg 1: 10:30AM  2) pkg6: 10:30AM  #) pkg 12,
def get_urgent_pkg_list():
    urgent_list = []
    for pkg in package_info_list:
        if pkg.get('deadline') != 'EOD':
            urgent_list.append(pkg.get('address') + ' ' + pkg.get('zip_code'))
            package_urgent_list.append(pkg)
    return urgent_list


route_for_urgent_delivery = find_fastest_route(start_location, get_urgent_pkg_list())


# print(route_for_urgent_delivery)


# Split packages and load into trucks. Each truck can carry a max of 16 packages. Trucks travel at 18 miles/hr
# special notes: 1) package 3 & 18 & 36 & 38: Can 0nly be on truck 2
#    2) package 6 & 25 & 28 & 32: Delayed on flight---will not arrive to depot until 9:05 am
#    3) package 9: Wrong address listed
#    4) package 14: Must be delivered with 15, 19,
#    5) package 16: Must be delivered with 13, 19
#    6) package 20: Must be delivered with 13, 15
#       (^package 14, 13, 15, 16, 19, 20 must be at the same truck^)
def load_cargo():
    for bucket in packageTable.table:
        for index, pkg in enumerate(bucket):
            if pkg[0] == 13 or pkg[0] == 14 or pkg[0] == 15 or pkg[0] == 16 or pkg[0] == 19 or pkg[0] == 20:
                truck1.append(vars(pkg[1]))
            if pkg[0] == 6 or pkg[0] == 25 or pkg[0] == 28 or pkg[0] == 32:
                truck2.append(vars(pkg[1]))

            # load urgent delivery packages to the first 2 trucks that will go out first, and split those packages to
            # two trucks so the drivers can take them as priority.
            size = len(package_urgent_list)
            for i in range(size):
                if truck1.count(package_urgent_list[i]) == 0 and len(truck1) < 16:
                    truck1.append(package_urgent_list[i])
                if i < size and truck1.count(package_urgent_list[i]) == 0:
                    truck2.append(package_urgent_list[i])
            if len(truck1) < 16:
                truck1.append(vars(pkg[1]))
            elif len(truck2) < 16:
                truck2.append(vars(pkg[1]))
            else:
                truck3.append(vars(pkg[1]))


# load package into each truck
load_cargo()

# print(tsp_shortest_path(truck1, start_location))
shortest_path = get_address_from_package_list(truck1, start_location)
print(shortest_path)


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
