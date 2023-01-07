import service
import HashTable

# Initialize an empty hashtable to store packages
packageTable = HashTable.ChainingHashTable()
# Initialize an empty dictionary to store the vertexes and edges of the graph
graph = {}

# Load data from csv files
service.LoadData(packageTable, graph)
# print(packageTable.table)

# Initialize three empty trucks
truck1 = []
truck2 = []
truck3 = []


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


# load package into each truck
load_cargo()


# find the distance between 2 locations
def calc_distance(route1, route2):
    graph_dict = dict(graph.get(route1))
    return graph_dict.get(route2)


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

    # Set the current location to the starting location
    current_location = start
    # Initialize an empty route
    route = [current_location]

    locations = []
    # get a list of just address of all packages
    for pkg in truck:
        locations.append(vars(pkg[1]).get("address") + " " + vars(pkg[1]).get("zip_code"))

    print(locations)
    print('+++')
    # Keep looping until all locations have been visited
    while locations:
        # Find the nearest unvisited location to the current location
        nearest_location = None
        nearest_distance = float('inf')
        for location in locations:
            location_distance = calc_distance(current_location, location)
            if location_distance != '':
                dist = float(location_distance)
            if dist < nearest_distance:
                nearest_location = location
                nearest_distance = dist

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
