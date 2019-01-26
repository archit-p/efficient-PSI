import random
import readerHash as RH
import sys
import os

class FileGenerator:

    """
        This class creates a single file.

        The class takes 3 parameters:
        1.) filepath -- The path of the raw file to write data to
        2.) num_elements -- The number of elements to write to the file
        3.) max_element_size -- The largest numerical value possible for the file entries

        The file structure is as follows:
        The first line represents num_elements elements
        Subsequent n_elements lines contain random values ranging from 0 to max_element_size-1

    """


    def __init__(self, filepath, num_elements, max_element_size):
        self.filepath = filepath
        self.num_elements = num_elements
        self.max_element_size = max_element_size


    def createFile(self):
        with open(self.filepath, 'w') as rawf:
            rawf.write(str(self.num_elements) + "\n")

            for i in range(0, self.num_elements):
                rawf.write(str(random.randint(0, self.max_element_size - 1)) + "\n")


def main():
	if not os.path.exists("../test/"):
		os.makedirs("../test/")
	# generate 7 files with data ranging from 10 elements to 10^7 elements
	for i in range(1, 8):
		num_ele = pow(10, i)
		fname1 = "../test/data" + str(i) + "_1.raw"
		rawf1 = FileGenerator(fname1, num_ele, num_ele<<2)
		rawf1.createFile()
		fname2 = "../test/data" + str(i) + "_2.raw"
		rawf2 = FileGenerator(fname2, num_ele, num_ele<<2)
		rawf2.createFile()
		print("Dataset " + str(i) + " --> generated!")
if __name__ == "__main__":
	main()

# Uncomment the below lines to view the buckets


# test1 = RH.fileReaderAndHash('datafile.raw',10000,1000000)
# print(test1.load_buckets())

# test2 = RH.fileReaderAndHash('datafile2.raw',10000,1000000)
# print(test2.load_buckets())
