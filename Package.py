import csv

import HashTable


# Deadline cases: 1) pkg 1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40: 10:30AM 2) pkg 15: 9:00AM 3) pkg 6: 10:30AM but
# pkg won't arrive to depot until 9:05AM special notes: 1) package 3 & 18 & 36 & 38: Can 0nly be on truck 2 and
# deadline is EOD 2) package 6 & 25 & 28 & 32: Delayed on flight -> will not arrive to depot until 9:05 am but pkg 6
# & 25 also require to be delivered before 10:30AM (urgent) 3) package 9: Wrong address listed 4) package 14: Must be
# delivered with 15, 19, 5) package 16: Must be delivered with 13, 19 6) package 20: Must be delivered with 13,
# 15 (^package 14, 13, 15, 16, 19, 20 must be at the same truck^)

class Package:
    package_table = HashTable.ChainingHashTable()

    # urgent means the deadline has a specific time except EOD
    all_package_info_list = []
    package_urgent_list = []
    package_urgent_delayed_list = []
    package_not_urgent_delayed_list = []
    package_with_wrong_address = []
    package_with_truck2_only = []
    package_must_on_same_truck = []
    package_remaining_packages = []

    def __init__(self, pkg_id, address, city, state, zip_code, deadline, weight, special_note, s_time='',
                 d_time="", distance=0, delivery_status='At The Hub'):
        self.pid = int(pkg_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note
        self.start_time = s_time
        self.delivery_time = d_time
        self.travel_distance = distance
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
        delay_msg = 'Delayed on flight---will not arrive to depot until 9:05 am'
        wrong_address = 'Wrong address listed'
        only_truck2 = 'Can only be on truck 2'

        for pkgs in self.package_table.table:
            for pkg in pkgs:
                self.all_package_info_list.append(vars(pkg[1]))
                must_on_same_truck_pkg = [13, 14, 15, 16, 19, 20]

                # Urgent delivery packages that already in the Hub, but not included the ones that has to be in the
                # same truck
                if vars(pkg[1]).get('deadline') != 'EOD' and vars(pkg[1]).get(
                        'special_note') == '' and must_on_same_truck_pkg.count(
                        vars(pkg[1]).get('pid')) < 1:
                    self.package_urgent_list.append(vars(pkg[1]))  # total of 7 out of 40
                # Urgent delivery packages that has not yet arrive
                elif vars(pkg[1]).get('deadline') != 'EOD' and vars(pkg[1]).get(
                        'special_note') == delay_msg:  # total of 2 out of 40
                    self.package_urgent_delayed_list.append(vars(pkg[1]))
                # packages that delayed but not require urgent delivery
                elif vars(pkg[1]).get('special_note') == delay_msg and vars(pkg[1]).get(
                        'deadline') == 'EOD':  # total of 2 out of 40
                    self.package_not_urgent_delayed_list.append(vars(pkg[1]))
                # packages that has to be with truck2
                elif vars(pkg[1]).get('special_note') == only_truck2:  # total of 4 out of 40
                    self.package_with_truck2_only.append(vars(pkg[1]))
                # packages with wrong address
                elif vars(pkg[1]).get('special_note') == wrong_address:  # total of 1 out of 40
                    self.package_with_wrong_address.append(vars(pkg[1]))
                # packages that must load together
                elif must_on_same_truck_pkg.count(vars(pkg[1]).get('pid')) > 0:  # total of 6 out of 40
                    self.package_must_on_same_truck.append(vars(pkg[1]))
                else:  # all remaining packages
                    self.package_remaining_packages.append(vars(pkg[1]))  # total of 15 of 40
    # @property
    # def start_time(self):
    #     return self._start_time
    #
    # @start_time.setter
    # def start_time(self, value):
    #     if value > int(8) * 60 + int(0):
    #         self._start_time = value
    #     else:
    #         raise Exception("Sorry, you can leave the hub no earlier than 8:00AM.")


    # # a format to display package info.
    # def __str__(self):
    #     return f'{self.pid} {self.address} {self.city} {self.state} {self.zip_code} {self.deadline} {self.weight} {self.special_note} {self.start_time()} {self.delivery_time} {self.status}'


