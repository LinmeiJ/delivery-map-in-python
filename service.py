
from Package import Package
import distance


class LoadData:

    # initialize data inside the constructor
    def __init__(self, packageTable, edges):
        pkg = Package(0, '', '', '', '', '', '', '', '', '', False)  # Create an instance of Package
        pkg.load_package_data('./resource/WGUPS Package File.csv', packageTable)

        # maps all the addresses and edges with giving data
        distance.Distance('./resource/WGUPS Distance Table.csv', edges)



