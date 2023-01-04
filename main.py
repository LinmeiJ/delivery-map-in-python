import csv

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
            print(row[0])
            hashTable.insert(int(row[0]),
                             Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6],
                                     row[7]))


packageTable = HashTable.ChainingHashTable()
load_package_data('./resource/WGUPS Package File.csv', packageTable)
print(packageTable.table)


