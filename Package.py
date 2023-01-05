import csv


class Package:

    def __init__(self, pkg_id, address, city, state, zip_code, deadline, weight, special_note, start_time="",
                 delivery_time="", delivery_status=False):
        self.pid = pkg_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note
        self.start_time = start_time
        self.delivery_time = delivery_time
        self.status = delivery_status

    @classmethod    # load package data from a csv file
    def load_package_data(cls, csv_file, hashTable):
        # read data from the WGUPS Package csv file
        with open(csv_file, "r") as pkgs:
            package_data = csv.reader(pkgs, delimiter=',')

            # Skip the header
            next(package_data)

            for row in package_data:
                # Create a new Package object and add it to the hash table
                pkg = cls(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                hashTable.insert(pkg.pid, pkg)

        # # for testing
        # def __str__(self):
        #     return f"{self.ID} {self.address} {self.city} {self.state} {self.zip} {self.deadline} {self.mass} {self.notes} {self.status} {self.time}"
