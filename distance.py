import csv


class Distance:
    def __init__(self, csv_file, adjacency_list):
        self.edges = adjacency_list

        with open(csv_file, 'r') as file:
            # Create a CSV reader object
            reader = csv.reader(file, delimiter=',')

            # Iterate over the rows of the CSV file
            for row in reader:
                # The first row contains the addresses
                if row[0] == "":
                    vertexs = row[3:] #addresses
                else:
                    # The first column of each row contains the destination addresses
                    destNode = row[0] + " " + row[1] + " " + row[2]
                    # The remaining columns contain the distances to the destination addresses
                    for address, distance in enumerate(row[3:]):  # addresses in first row in csv file
                        # Get the destination address
                        vertex = vertexs[address]
                        # Add the edge to the dictionary: key is the starting address, value is a list of destination addresses and the distance from the starting address
                        if vertex not in self.edges:
                            self.edges[vertex] = [(destNode, distance)]
                        else:
                            self.edges[vertex].append((destNode, distance))


    # def dijkstra_shortest_path(graph, src, dest):
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