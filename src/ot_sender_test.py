from ot_sender import OTSender
import socket
import random
import pickle
from fastecdsa import keys,curve, ecdsa
import cProfile
import readerHash as RH
import setIntersect as SI
from sys import argv

def ot_sender_test(srv_port,buckets):
    result = 0
    sender_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sender_s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    fail_count = 0
    sender_s.connect(("localhost",srv_port))
    count_ot = 0
    print("Performing OT")
    intersection = set()
    for numbers in buckets:
        len_a = len(numbers)
        sender_s.send(str(len_a).encode('utf-8'))
        len_b = int(sender_s.recv(32))
        print("Received length of bucket is " + str(len_b))
        
        # initialize result array to false
        result_array = [[False for x in range(len_b)] for y in range(len_a)]
        for i in range(len_b):
            for j in range(len_a):
                num_cpy = numbers[j]
                result = 0
                str_list = []
                for k in range(0,32):
                    bit = num_cpy&1
                    num_cpy = num_cpy >> 1
                    rand_str = list()

                    rand_str.append(random.randint(10000000,20000000))
                    rand_str.append(random.randint(10000000,20000000))

                    result = result ^ rand_str[bit]

                    while True:
                        count_ot += 1
                        obj = OTSender(str(rand_str[0]), str(rand_str[1]), 4444, sender_s)
                        ka = keys.export_key(obj.A, curve.P256)
                        sender_s.send(ka.encode('ASCII'))
                        data = sender_s.recv(512)
                        if(data != b'ERROR'):
                            break
                    
                    while True:
                        try:
                            B = keys.import_key_str(data.decode('ASCII'))[1]
                            break
                        except:
                            sender_s.send(b"ERROR")
                            data = sender_s.recv(512)
                            fail_count += 1

                    ciphers = obj.sender_keygen(B)
                    cipher_linear = pickle.dumps(ciphers)
                    sender_s.send(cipher_linear)
                
                #print("Result is = " + str(result))
                sender_s.send(str(result).encode('utf-8'))
                serv_result = int(sender_s.recv(512))
                result_array[j][i] = (result == serv_result)
                if(result_array[j][i] == True):
                    print("Adding {} to intersection!".format(numbers[j]))
                    intersection.add(numbers[j])
        print(result_array)
    print("Intersection is = ")
    print(intersection)
    print("Number of OT Senders = {}".format(count_ot))

def main():
    if(len(argv) != 3):
        print("Usage: python3 driver.py <filename1> <num-buckets>");
        return None

    num_b = int(argv[2])

    test1 = RH.fileReaderAndHash(argv[1],num_b)
    buckets = test1.load_buckets()
    ot_sender_test(4444, buckets)
    #cProfile.runctx('ot_sender_test(4444, buckets)',locals(),globals())

if __name__ == "__main__":
    main()
