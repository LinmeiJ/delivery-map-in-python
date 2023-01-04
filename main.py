import csv
import heapq

import HashTable
from Package import Package

print('WGU Delivery APP')


# load data from a csv file
def load_package_data(csv_file, hashTable):
    # read data from the WGUPS Package csv file
    with open(csv_file, "r") as pkgs:
        package_data = csv.reader(pkgs, delimiter=',')

        # Skip the header
        next(package_data)
        for row in package_data:
            # Add the package data to the hash table
            hashTable.insert(int(row[0]),
                             Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6],
                                     row[7]))


packageTable = HashTable.ChainingHashTable()
load_package_data('./resource/WGUPS Package File.csv', packageTable)
# print(packageTable.table)


# Open the CSV file
with open('./resource/WGUPS Distance Table.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Initialize an empty list to store the data
    data = []

    # Iterate over the rows of the CSV file
    for row in reader:
        data.append(row)

    # for i in data:
    #     print(i)

    # Initialize an empty graph
graph = {}

# Iterate over the rows of the data
for row in data:
    # Get the source and destination nodes and the distance
    src = row[0]
    print(src)
    dest = row[1]
    distance = row[3]
    print(f"{dest} EEEEEND  {distance}")

    # Add the edge to the graph
    if src not in graph:
        graph[src] = [(dest, distance)]
    else:
        graph[src].append((dest, distance))

### continue to store more edges

    # Add the edge to the graph
if src not in graph:
    graph[src] = [(dest, distance)]
else:
    graph[src].append((dest, distance))


def dijkstra(graph, src, dest):
    # Initialize a priority queue to store the distances and nodes
    queue = []
    # Push the source node into the queue with a distance of 0
    heapq.heappush(queue, (0, src))
    # Initialize a dictionary to store the distances from the source node
    distances = {}
    # Set the distance of the source node to 0
    distances[src] = 0
    # Initialize a dictionary to store the predecessor nodes
    predecessors = {}

    # Repeat the following until the queue is empty
    while queue:
        # Pop the node with the smallest distance from the queue
        distance, node = heapq.heappop(queue)
        # If the node is the destination, return the distances and predecessors
        if node == dest:
            return distances, predecessors
        # Iterate over the neighbors of the node
        for neighbor, edge_distance in graph[node]:
            # Calculate the total distance to the neighbor
            total_distance = distance + edge_distance


