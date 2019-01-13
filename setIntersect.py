import math

class twoSetIntersection:

	def __init__(self, set1, set2):
		self.set1 = set1
		self.set2 = set2
		self.set1_num_buckets = int(set1.max_element_size/set1.bucket_size)
		self.set2_num_buckets = int(set2.max_element_size/set2.bucket_size)
		self.intersected_list = list()

	def create_intersection(self):

		for i in range(0,min(self.set1_num_buckets, self.set2_num_buckets)):
			lst1 = self.set1.bucket_array[i]
			lst2 = self.set2.bucket_array[i]

			lst3 = [element for element in lst1 if element in lst2]

			for element in lst3:
				self.intersected_list.append(element)

		return self.intersected_list