import csv


class Package:
    # def __init__(self, package_id, delivery_address, delivery_deadline, delivery_city, delivery_zip_code,
    #              delivery_weight, delivery_status=False):
    #     self.package_id_number = package_id
    #     self.delivery_address = delivery_address
    #     self.delivery_deadline = delivery_deadline
    #     self.delivery_city = delivery_city
    #     self.delivery_zip_code = delivery_zip_code
    #     self.weight = delivery_weight
    #     self.status = delivery_status

    def __init__(self, csv_file):
        self.packages = {}

        # read data from the csv file
        with open(csv_file, "r") as f:
            package_data = csv.DictReader(f)
            # next(package_data)
            for row in package_data:
                # Add the package data to the hash table
                self.packages[row['Package ID']] = [row['Address'], row['City'], row['State'], row['ZipCode'],
                                                    row['Deadline'], row['Weight'], row['Special Notes']]


