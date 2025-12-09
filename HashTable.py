class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity 
        self.table = [] * capacity

    # hash function, simple modulo of key with capacity
    def hash(self, key):
        return key % self.capacity
    
    # insert package or update current one
    def insert(self, key, value):
        bucket_index = self.hash(key)
        bucket = self.table[bucket_index]

        for item in bucket:
            if item[0] == key:
                item[1] = value
                return
            
        # append new key-value if pair not found 
        bucket.append([key, value])
    
    # lookup package data by key 
    def lookup(self, key):
        bucket_index = self.hash(key)
        bucket = self.table[bucket_index] 

        for item in bucket:
            if item[0] == key:
                return item[1] 
        
        return None # key not found