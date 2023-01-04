#Instead of using a dictionary to store the graph, you can also use a matrix to represent the graph.
# To do this, you can create a 2D list or array where each element matrix[i][j] represents the distance between node i and node j.
# If there is no edge between the two nodes,
# you can set the element to a large value such as float('inf').

import csv

# Open the CSV file
with open('delivery_data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Initialize a list of the unique nodes in the graph
    nodes = set()

    # Iterate over the rows of the CSV file
    for row in reader:
        # Add the source and destination nodes to the list
        nodes.add(row[0])
        nodes.add(row[1])

# Create an adjacency matrix with the correct size
num_nodes = len(nodes)
matrix = [[float('inf') for _ in range(num_nodes)] for _ in range(num_nodes)]

# Open the CSV file again
with open('delivery_data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Iterate over the rows of the CSV file
    for row in reader:
        # Get the source and destination indices and the distance
        src_index = list(nodes).index(row[0])
        dest_index = list(nodes).index(row[1])
        distance = int(row[2])
        # Set the distance in the matrix
        matrix[src_index][dest_index] = distance

# The matrix is now a 2D list or array where each element matrix[i][j] represents the distance between node i and node j


def dijkstra(matrix, src_index, dest_index):
    # Initialize a priority queue to store the distances and nodes
    queue = []
    # Push the source node into the queue with a distance of 0
    heapq.heappush(queue, (0, src_index))
    # Initialize a list to store the distances from the source node
    distances = [float('inf') for _ in range(num_nodes)]
    # Set the distance of the source node to 0
    distances[src_index] = 0
    # Initialize a list to store the predecessor nodes
    predecessors = [-1 for _ in range(num_nodes)]

    # Repeat the following until the queue is empty
    while queue:
        # Pop the node with the smallest distance from the queue
        distance, node_index = heapq.heappop(queue)
        # If the node is the destination, return the distances and predecessors
        if node_index == dest_index:
            return distances, predecessors
        # Iterate over the neighbors of the node
