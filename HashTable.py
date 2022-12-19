# The implementation is referenced from 'Hash Table class using Chaining' in ZyBook Chapter 9'
class HashTable:

    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def addData(self, key, value):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if self.searchKey(key) == key:
            self.table[key] = value

        else:
            dic = [key, value]
            bucket_list.append(dic)

    def searchKey(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        if key in bucket_list:
            bucket_list.remove(key)
