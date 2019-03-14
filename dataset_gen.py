import random
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
	if not os.path.exists("./test"):
		os.makedirs("test")
    max_p = sys.argv[1]
    print("Generating datasets from 2 to 2^{} elements!")
	# generate 20 files with data ranging from 10 elements to 200 elements elements
	for i in range(maxp):
		num_ele = pow(2,i+1)
		fname1 = "./test/data" + str(i+1) + "_1.raw"
		rawf1 = FileGenerator(fname1, num_ele, num_ele<<2)
		rawf1.createFile()
		fname2 = "./test/data" + str(i+1) + "_2.raw"
		rawf2 = FileGenerator(fname2, num_ele, num_ele<<2)
		rawf2.createFile()
		print("Dataset " + str(i+1) + " --> generated!")

if __name__ == "__main__":
	main()
