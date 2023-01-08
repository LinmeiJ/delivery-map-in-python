import csv


class Graph:
    def __init__(self, csv_file, adjacency_list):
        self.edges = adjacency_list

        with open(csv_file, 'r') as file:
            # Create a CSV reader object
            reader = csv.reader(file, delimiter=',')

            # Iterate over the rows of the CSV file
            for row in reader:
                # The first row contains the addresses
                if row[0] == "":
                    vertexes = row[2:]  # addresses
                else:
                    # The first column of each row contains the destination addresses
                    dest_node = row[0] + " " + row[1]
                    # The remaining columns contain the distances to the destination addresses
                    for i, distance in enumerate(row[2:]):  # addresses in first row in csv file
                        # Get the destination address start from index 0
                        vertex = vertexes[i]
                        # Add the edge to the dictionary: key is the starting address, value is a dictionary of
                        # destination addresses and distances from the starting address
                        if vertex not in self.edges:
                            self.edges[vertex] = [(dest_node, distance)]
                        else:
                            self.edges[vertex].append((dest_node, distance))

        # Driver can drive to location B from A, also can drive from A to B. The following is to add missing
        # distance data from B to A, for instance, as the csv only proves distance from A to B
        start = '4001 South 700 East 84107'
        for k, v in self.edges.items():
            if k == start:
                pass
            else:
                for dest in v:
                    if dest[1] == '':
                        edge_list = self.edges.get(dest[0])
                        for address in edge_list:
                            if address[0] == k:
                                dest[1] = address[1]
                                break  # once find the distance, break the loop
                    else:
                        break  # only access missing data destination, skip the ones already have distance
                        # assigned to it
