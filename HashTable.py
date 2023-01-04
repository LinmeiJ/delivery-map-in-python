# The implementation is referenced from 'Hash Table class using Chaining' in ZyBook Chapter 9'
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new pair into the hash table.
    def insert(self, key, value):
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # return true when the pair is already exits
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = value
                return True
        # insert the pair into table when it doesn't exit
        pair = [key, value]
        bucket_list.append(pair)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket number
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for kv in bucket_list:
            # find the key and return its value
            if kv[0] == key:
                return kv[1]
        return None  # None means not found

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            if (kv[0]) == key:
                bucket_list.remove(key[0], key[1])
