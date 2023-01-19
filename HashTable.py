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
    # Time complexity: O(n) >> the number of elements in the bucket where the key value pair is being inserted
    # Space complexity: 0(1)
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
    # Time complexity: O(1) on average, O(n) as the worst case. (More explanation is in the document)
    # Space complexity: 0(1) >> just require a constant amount of memory regardless of the number of key value pair in the bucket.
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
    # Time complexity: O(n) >> where n is the max size of number of elements in the bucket list with a linear search approach.
    # Space complexity: 0(1) >> just require a constant amount of memory
    def remove(self, key):
        # get the bucket where this item will be removed from.
        bucket = self.find_bucket(key)

        # remove the item from the bucket list if it is present.
        for kv in bucket:
            if (kv[0]) == key:
                bucket.remove(kv)

    # Time complexity: O(n) >> where n is the max size of number of element in the bucket
    # Space complexity: 0(1) >> just require a constant amount of memory
    def update_pkg_delivery_status(self, key, status):
        bucket = self.find_bucket(key)
        for element in bucket:
            if (element[0]) == key:
                setattr(element[1], 'status', status)

    # Time and space complexity both are O(1)
    def find_bucket(self, key):
        bucket = hash(key) % len(self.table)
        return self.table[bucket]
