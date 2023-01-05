import csv

import Graph
import HashTable
from Package import Package


class Services:
    packageTable = HashTable.ChainingHashTable()

    # Initialize an empty dictionary to store the edges of the graph
    edges = {}

    def __init__(self):
        pkg = Package(0, '', '', '', '', '', '', '', '', '', False)
        pkg.load_package_data('./resource/WGUPS Package File.csv', self.packageTable)
        # print(self.packageTable.table)

        g = Graph.Graph('./resource/WGUPS Distance Table.csv', self.edges)
        # print(g.edges)
        print(g.edges.values())

# def dijkstra(graph, src, dest):
#     # Initialize a priority queue to store the distances and nodes
#     queue = []
#     # Push the source node into the queue with a distance of 0
#     heapq.heappush(queue, (0, src))
#     # Initialize a dictionary to store the distances from the source node
#     distances = {}
#     # Set the distance of the source node to 0
#     distances[src] = 0
#     # Initialize a dictionary to store the predecessor nodes
#     predecessors = {}
#
#     # Repeat the following until the queue is empty
#     while queue:
#         # Pop the node with the smallest distance from the queue
#         distance, node = heapq.heappop(queue)
#         # If the node is the destination, return the distances and predecessors
#         if node == dest:
#             return distances, predecessors
#         # Iterate over the neighbors of the node
#         for neighbor, edge_distance in graph[node]:
#             # Calculate the total distance to the neighbor
#             total_distance = distance + edge_distance
