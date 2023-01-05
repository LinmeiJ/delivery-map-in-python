import csv


class Graph:
    def __init__(self, csv_file, edges):
        self.edges = edges
        with open(csv_file, 'r') as file:
            # Create a CSV reader object
            reader = csv.reader(file, delimiter=',')

            # Iterate over the rows of the CSV file
            for row in reader:
                # The first row contains the addresses
                if row[0] == "":
                    addresses = row[3:]
                    # print(addresses)
                else:
                    # The first column of each row contains the source address
                    dest = row[0] + " " + row[1] + " " + row[2]
                    # The remaining columns contain the distances to the destination addresses
                    for i, distance in enumerate(row[3:]):  # addresses in first row in csv file
                        # Get the destination address
                        src = addresses[i]
                        # Add the edge to the dictionary
                        if src not in self.edges:
                            self.edges[src] = [(dest, distance)]
                        else:
                            self.edges[src].append((dest, distance))