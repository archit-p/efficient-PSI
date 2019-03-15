import math
import time

class fileReaderAndHash:

    """
        This module contains a class named fileReaderAndHash.

        The class constructor accepts 3 params :
            1.) filepath -- The path of the raw file to read data from
            2.) bucket_size -- size of each bucket
            3.) max_element_size -- The largest numerical value of the element

        The class contains attribute buckets as the bucket containing the hashed elements from the file
        The other attibutes are used for timing and benchmarking facilities.
        Time Benchmarking variables use 2 fields -- Real Time and Process Time. Real time is the actual time spent to run the segment of the code.
        Process time is the time spent inside CPU not including the time spent in context switching and process on sleep by OS

        The class contains 2 methods:
            1.) load_buckets -- This carries out actual loading of data from the raw files to the buckets in memory. Returns the buckets
            2.) timing_stats -- Prints the timing stats and also returns an array containing the timing stats
    """

    def __init__(self, filepath, num_buckets):
        self.filepath = filepath
        self.num_buckets = num_buckets
        self.buckets = list()

    def get_hash(self, token):
        hash = 0
        for i in range(len(token)):
            hash += int(token[i])
            hash += (hash << 10)
            hash ^= (hash >> 6)
        hash += (hash << 3)
        hash ^= (hash >> 11)
        hash += (hash << 15)

        return hash

    def load_buckets(self):
        with open(self.filepath, 'r') as rawf:
            num_elements = int(rawf.readline())

            for i in range(self.num_buckets):
                a = list()
                self.buckets.append(a)
            
            for line in rawf:
                element = line.strip()
                index = self.get_hash(element) % self.num_buckets
                self.buckets[index].append(int(element))
        return self.buckets
                