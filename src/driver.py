import readerHash as RH
import setIntersect as SI
from sys import argv


def main():
	if(len(argv) != 5):
		print("Usage: python3 driver.py <filename1> <filename2> <bucket-size> <max-elem-size>");
		return None
	
	bsize = int(argv[3])
	elemsize = int(argv[4])

	test1 = RH.fileReaderAndHash(argv[1],bsize,elemsize)
	test1.load_buckets()

	test2 = RH.fileReaderAndHash(argv[2],bsize,elemsize)
	test2.load_buckets()

	test_intersect = SI.twoSetIntersection(test1,test2)
	print(test_intersect.create_intersection())

if __name__ =="__main__":
	main()
