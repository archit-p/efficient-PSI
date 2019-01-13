import readerHash as RH
import setIntersect as SI

test1 = RH.fileReaderAndHash('datafile.raw',10000,1000000)
print(test1.load_buckets())

test2 = RH.fileReaderAndHash('datafile2.raw',10000,1000000)
print(test2.load_buckets())

test_intersect = SI.twoSetIntersection(test1,test2)
print(test_intersect.create_intersection())