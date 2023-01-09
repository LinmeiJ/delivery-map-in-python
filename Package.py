import csv

import HashTable


# Deadline cases: 1) pkg 1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40: 10:30AM
# 2) pkg 15: 9:00AM
# 3) pkg 6: 10:30AM but pkg won't arrive to depot until 9:05AM

class Package:

    package_table = HashTable.ChainingHashTable()

    all_package_info_list = []
    all_package_address_list = []
    package_urgent_list = []
    package_urgent_list_address_only = []
    package_flight_delayed_list = []
    package_remaining_packages = []
    package_with_wrong_address = []

    def __init__(self, pkg_id, address, city, state, zip_code, deadline, weight, special_note, start_time="",
                 delivery_time="", delivery_status='At The Hub'):
        self.pid = int(pkg_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note
        self._start_time = start_time
        self.delivery_time = delivery_time
        self.status = delivery_status

    # load package data from a csv file and category them
    def load_package_data(self):
        # read data from the WGUPS Package csv file
        with open('./resource/WGUPS Package File.csv', "r") as pkgs:
            package_data = csv.reader(pkgs, delimiter=',')

            # Skip the header
            next(package_data)

            for row in package_data:
                # Create a new Package object and add it to the hash table
                pkg = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

                self.package_table.insert(pkg.pid, pkg)
        self.category_packages()

    def category_packages(self):
        for pkgs in self.package_table.table:
            for pkg in pkgs:
                self.all_package_address_list.append(vars(pkg[1]).get('address') + ' ' + vars(pkg[1]).get('zip_code'))
                self.all_package_info_list.append(vars(pkg[1]))
                # urgent delivery packages
                if vars(pkg[1]).get('deadline') != 'EOD':
                    self.package_urgent_list_address_only.append(vars(pkg[1]).get('address') + ' ' + vars(pkg[1]).get('zip_code'))
                    self.package_urgent_list.append(pkg)
                # packages with special notes
                elif vars(pkg[1]).get('special_note') == 'Delayed on flight---will not arrive to depot until 9:05 am':
                    self.package_flight_delayed_list.append(pkg)
                elif vars(pkg[1]).get('special_note') == 'package_with_wrong_address':
                    self.package_with_wrong_address.append(pkg)
                # all remaining packages
                else:
                    self.package_remaining_packages.append(pkg)

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        if value > int(8) * 60 + int(0):
            self._start_time = value
        else:
            raise Exception("Sorry, you can leave the hub no earlier than 8:00AM.")

    @property
    def delivery_time(self):
        return self._start_time

    @delivery_time.setter
    def delivery_time(self, value):
        self._delivery_time = value

    @property
    def status_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    # # a format to display package info.
    # def __str__(self):
    #     return f'{self.pid} {self.address} {self.city} {self.state} {self.zip_code} {self.deadline} {self.weight} {self.special_note} {self.start_time()} {self.delivery_time} {self.status}'

    # start_time = int(start_hour)*60 + int(start_minute)
    # end_time = int(end_hour)*60 + int(end_minute)
    # current_time =  datetime.now().hour*60 +datetime.now().minute
    # if start_time <= current_time and end_time >= current_time:
    # doSomething
