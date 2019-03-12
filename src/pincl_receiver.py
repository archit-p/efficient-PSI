import socket
import sys
sys.path.append('../test/')

from peq_receiver import peq_test_receiver
from readerHash import fileReaderAndHash


def printIntersection(intersection):
    for b_index, bucket in enumerate(intersection):
        print("Bucket {}:".format(b_index))
        for element in bucket:
            print("Element: ", element)

    return


def pincl_test_receiver(buckets, bsize, elemsize, port):
    intersection = [[] for _ in range(len(buckets))]

    for b_index, bucket in enumerate(buckets):
        for element in bucket:
            print("checking for element ", element)
            result = peq_test_receiver(element, port)
            if result:
                intersection[b_index].append(element)

    printIntersection(intersection)

    return intersection

def main():
    # size of bucket
    bsize = 3

    # maximum size of element
    elemsize = 20 

    test1 = [[1, 2, 3], [2, 4, 5]]

    # test1 = fileReaderAndHash("data1_1.raw", bsize, elemsize)
    # test1.load_buckets()

    pincl_test_receiver(test1, bsize, elemsize, 4444)


if __name__ == "__main__":
    main()