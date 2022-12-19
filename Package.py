import csv
import itertools

from HashTable import HashTable


def initialize_package_data():
    with open('./resource/WGUPS Package File.csv', 'r') as file:
        cvs_file = csv.DictReader(file)
        for line in cvs_file:
            # print(line)
            # package = Package(line['Package ID'], line['Address'], line['City'], line['State'], line['ZipCode'],
            #                   line['Deadline'], line['Weight'], line['Special Notes'])
            HashTable().addData(int(line['Package ID']), dict(itertools.islice(line.items(), 2, None)))
            # HashTable.addData(package)

            HashTable().remove(1)
class Package:

    def __init__(self, package_id, delivery_address, delivery_deadline, delivery_city, delivery_zipcode,
                 delivery_weight, delivery_status=False):
        self.ID = package_id
        self.address = delivery_address
        self.deadline = delivery_deadline
        self.city = delivery_city
        self.zipcode = delivery_zipcode
        self.weight = delivery_weight
        self.status = delivery_status

    def __init__(self, package_id, delivery_address, delivery_city, delivery_state, delivery_zipcode, delivery_deadline,
                 delivery_weight, delivery_special_notes):
        self.ID = package_id
        self.address = delivery_address
        self.city = delivery_city
        self.city = delivery_state
        self.zipcode = delivery_zipcode
        self.deadline = delivery_deadline
        self.weight = delivery_weight
        self.special_note = delivery_special_notes
