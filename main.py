import csv

from Package import Package

print('WGU Delivery APP')

pkg = Package('./resource/WGUPS Package File.csv')
print(pkg.packages)
