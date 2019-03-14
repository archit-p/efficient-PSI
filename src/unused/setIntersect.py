import math

class twoSetIntersection:

	def __init__(self, set1, set2):
		self.set1 = set1
		self.set2 = set2
		self.set1_num_buckets = int(set1.num_buckets)
		self.set2_num_buckets = int(set2.num_buckets)
		self.intersected_list = list()

	def create_intersection(self):
		for i in range(0,min(self.set1_num_buckets, self.set2_num_buckets)):
			lst1 = {}
			lst2 = {}
			lst1 = self.set1.buckets[i]
			lst2 = self.set2.buckets[i]

			lst3 = [element for element in lst1 if element in lst2]

			for element in lst3:
				self.intersected_list.append(element)

		return self.intersected_list
