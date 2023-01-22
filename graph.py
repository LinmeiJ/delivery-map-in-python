import csv


# This class reads graphical data from a CSV file and store it as a list of dictionary.
class Graph:
    address_with_distance = {}

    # Time complexity: O(RC) >> where R represents the number of rows and C represents the number of columns in the CSV file.
    # Space complexity: O(RC) >> the address_with_distance directionary is populated with RC key-value pairs. where R is the number of rows and C is the number of columns from CSV file.
    def __init__(self):
        with open('./resource/WGUPS Distance Table.csv', 'r') as file:
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
                        if vertex not in self.address_with_distance:
                            self.address_with_distance[vertex] = [[dest_node, distance]]
                        else:
                            self.address_with_distance[vertex].append([dest_node, distance])

        # Driver can drive to location B from A, also can drive from A to B. The following is to add missing
        # distance data from B to A as reading the csv file only fill up distance data from one direction
        start = '4001 South 700 East 84107'

        # Time complexity: O(AD^2) >> where A represents the number of addresses and D is the number of destinations of each address
        # Space complexity: O(1) >> just a constant amount of memory regardless of the size of the input
        for k, v in self.address_with_distance.items():
            if k == start:
                pass
            else:
                for dest in v:
                    if dest[1] == '':
                        edge_list = self.address_with_distance.get(dest[0])
                        for address in edge_list:
                            if address[0] == k:
                                dest[1] = address[1]
                                break  # once find the distance, break the loop
                    else:
                        break  # only access missing data destination, skip the ones already have distance
                        # assigned to it
