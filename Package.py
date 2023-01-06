import csv


class Package:

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
        self._delivery_time = delivery_time
        self._status = delivery_status

    @classmethod  # load package data from a csv file
    def load_package_data(cls, csv_file, hashTable):
        # read data from the WGUPS Package csv file
        with open(csv_file, "r") as pkgs:
            package_data = csv.reader(pkgs, delimiter=',')

            # Skip the header
            next(package_data)

            for row in package_data:
                # Create a new Package object and add it to the hash table
                pkg = cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

                hashTable.insert(pkg.pid, pkg)

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        if value > int(8) * 60 + int(0):
            self._start_time = value
        else:
            raise Exception("Sorry, you can leave the hub no earlier than 8:00AM.")
    # start_time = int(start_hour)*60 + int(start_minute)
    # end_time = int(end_hour)*60 + int(end_minute)
    # current_time =  datetime.now().hour*60 +datetime.now().minute
    # if start_time <= current_time and end_time >= current_time:
    # doSomething

    @property
    def delivery_time(self):
        return self._start_time

    @delivery_time.setter
    def delivery_time(self, value):
        self._delivery_time = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    # # for testing
    # def __str__(self):
    #     return f"{self.ID} {self.address} {self.city} {self.state} {self.zip} {self.deadline} {self.mass} {self.notes} {self.status} {self.time}"
