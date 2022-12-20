import csv

from Graph import Graph
from Package import Package

print('WGU Delivery APP')

# Create an instance of the Package class, passing in the path to the CSV file
pkg = Package('./resource/WGUPS Package File.csv')
# print(pkg.packages)

# Create an instance of the Graph class, passing in the path to the CSV file
graph = Graph('./resource/WGUPS Distance Table.csv')
print(graph.matrix)
print(graph.matrix[1][4])    # [row][column]. row[0] = row1 and column[0] = column 1 in excel sheet