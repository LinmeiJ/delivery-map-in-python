import csv

import HashTable


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

    # for testing
    def __str__(self):
        return f"{self.ID} {self.address} {self.city} {self.state} {self.zip} {self.deadline} {self.mass} {self.notes} {self.status} {self.time}"
