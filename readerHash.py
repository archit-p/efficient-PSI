import math
import time

class fileReaderAndHash:

	"""
		This module contains a class named fileReaderAndHash.

		The class constructor accepts 3 params :
			1.) filepath -- The path of the raw file to read data from
			2.) bucket_size -- size of each bucket
			3.) max_element_size -- The largest numerical value of the element

		The class contains attribute bucket_array as the bucket containing the hashed elements from the file
		The other attibutes are used for timing and benchmarking facilities.
		Time Benchmarking variables use 2 fields -- Real Time and Process Time. Real time is the actual time spent to run the segment of the code.
		Process time is the time spent inside CPU not including the time spent in context switching and process on sleep by OS

		The class contains 2 methods:
			1.) load_buckets -- This carries out actual loading of data from the raw files to the buckets in memory. Returns the bucket_array
			2.) timing_stats -- Prints the timing stats and also returns an array containing the timing stats
	"""

	def __init__(self, filepath, bucket_size, max_element_size):
		self.filepath = filepath
		self.bucket_size = bucket_size
		self.max_element_size = max_element_size
		self.bucket_array = dict()
		self.bucket_loading_time = {'real_time':-1, 'process_time':-1}
		self.hashing_to_bucket_time = {'real_time':-1, 'process_time':-1}
		self.bucket_array_creation_time = {'real_time':-1, 'process_time':-1}

	def load_buckets(self):
		rs1 = time.time()
		ps1 = time.process_time()
		with open(self.filepath, 'r') as rawf:
			num_elements = int(rawf.readline())

			rs2 = time.time()
			ps2 = time.process_time()
			for i in range(0,int(self.max_element_size/self.bucket_size)):
				self.bucket_array[i] = list()
			re2 = time.time()
			pe2 = time.process_time()

			rs3 = time.time()
			ps3 = time.process_time()
			for line in rawf:
				element = int(line)
				self.bucket_array[math.floor(element / self.bucket_size)].append(element)
			re3 = time.time()
			pe3 = time.process_time()
		re1 = time.time()
		pe1 = time.process_time()

		self.bucket_loading_time['real_time'] = (re1 - rs1)*1000
		self.hashing_to_bucket_time['real_time'] = (re2 - rs2)*1000
		self.bucket_array_creation_time['real_time'] = (re3 - rs3)*1000

		self.bucket_loading_time['process_time'] = (pe1 - ps1)*1000
		self.hashing_to_bucket_time['process_time'] = (pe2 - ps2)*1000
		self.bucket_array_creation_time['process_time'] = (pe3 - ps3)*1000

		return self.bucket_array

	def timing_stats(self):
		print("The Timing Stats on the fileReaderAndHash\n")
		print("Real Bucket Loading Time:" + str(self.bucket_loading_time['real_time']) + " ms\n")
		print("Real Hashing to bucket Time:" + str(self.hashing_to_bucket_time['real_time']) + " ms\n")
		print("Real Bucket Array Creation Time:" + str(self.bucket_array_creation_time['real_time']) + " ms\n")

		print("Process Bucket Loading Time:" + str(self.bucket_loading_time['process_time']) + " ms\n")
		print("Process Hashing to bucket Time:" + str(self.hashing_to_bucket_time['process_time']) + " ms\n")
		print("Process Bucket Array Creation Time:" + str(self.bucket_array_creation_time['process_time']) + " ms\n")
		
		return {'bucket_loading_time':self.bucket_loading_time, 'hashing_to_bucket_time':self.hashing_to_bucket_time,'bucket_array_creation_time':self.bucket_array_creation_time}