# The reference for the following implementation is from 'Hash Table class using Chaining' in ZyBook Chapter 9
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # radix sort algorithm to store packages in hash table
    # Inserts a new pair into the hash table.
    def insert(self, key, value):
        bucket = self.find_bucket(key)

        # return true when the pair is already exits
        for kv in bucket:
            if kv[0] == key:
                kv[1] = value
                return True
        # insert the pair into table when it doesn't exit
        pair = [key, value]
        bucket.append(pair)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket number
        bucket = self.find_bucket(key)

        # search for the key in the bucket list
        for kv in bucket:
            # find the key and return its value
            if kv[0] == key:
                return kv[1]
        return None  # None means not found

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket where this item will be removed from.
        bucket = self.find_bucket(key)

        # remove the item from the bucket list if it is present.
        for kv in bucket:
            if (kv[0]) == key:
                bucket.remove(kv)

    def update_pkg_delivery_status(self, key, status):
        bucket = self.find_bucket(key)
        for element in bucket:
            if (element[0]) == key:
                setattr(element[1], 'status', status)

    def find_bucket(self, key):
        bucket = hash(key) % len(self.table)
        return self.table[bucket]
