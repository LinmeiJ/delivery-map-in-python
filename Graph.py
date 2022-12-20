import csv


class Graph:
    def __init__(self, csv_file):
        self.matrix = []

        # Open the CSV file and read the data
        with open(csv_file, "r") as f:
            location_distance_data = csv.reader(f)
            for row in location_distance_data:
                # Add the distance data to the matrix
                self.matrix.append(row)
