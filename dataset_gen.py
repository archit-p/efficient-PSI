import random
import readerHash as RH

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




rawf1 = FileGenerator('datafile.raw', 1000000, 1000000)
rawf1.createFile()

rawf2 = FileGenerator('datafile2.raw', 1000000, 1000000)
rawf2.createFile()

# Uncomment the below lines to view the buckets


# test1 = RH.fileReaderAndHash('datafile.raw',10000,1000000)
# print(test1.load_buckets())

# test2 = RH.fileReaderAndHash('datafile2.raw',10000,1000000)
# print(test2.load_buckets())
