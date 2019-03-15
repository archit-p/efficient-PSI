from ot_receiver import OTReceiver 
import socket
import random
from fastecdsa import keys,curve, ecdsa
import pickle
import encrypt
import time
import cProfile
import reader_hash as RH
from sys import argv

def ot_receiver_test(port, buckets):
    count_ot = 0
    receiver_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver_s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    receiver_s.bind(('127.0.0.1', port))
    receiver_s.listen()
    print("listening on port " + str(port))
    conn, addr = receiver_s.accept()
    # use bits of the number as choice bits
    print("received connection from " +  str(addr))
    fail_count = 0
    intersection = set()

    for numbers in buckets:
        len_b = int(conn.recv(32))
        len_a = len(numbers)
        print("Received length of buckets is " + str(len_b))

        conn.send(str(len_a).encode('utf-8'))
        result_array = [[False for x in range(len_b)] for y in range(len_a)]

        for i in range(len_a):
            for j in range(len_b):
                num_cpy = numbers[i]
                result = 0
                #before starting equality send the length of a bucket
                # equality for a given number
                for k in range(0,32):
                    bit = num_cpy & 1
                    num_cpy = num_cpy >> 1
                    while True:
                        try:
                            data = conn.recv(512)
                            A = keys.import_key_str(data.decode('ASCII'))[1]
                            break
                        except:
                            conn.send(b"ERROR")
                            fail_count += 1

                    # send B
                    while True:
                        count_ot += 1
                        obj = OTReceiver(bit, receiver_s)
                        obj.set_B(A)
                        bk = keys.export_key(obj.B, curve.P256)
                        conn.sendall(bk.encode('ASCII'))
                        data = conn.recv(512)
                        if(data != b'ERROR'):
                            break

                    kr = A*obj.b
                    key_hashed_r = encrypt.getHash(str(kr).encode('utf-8'))
                    choice_cipher = "e" + str(bit)
                    cipher = pickle.loads(data)
                    msg = encrypt.decipher(key_hashed_r, cipher[choice_cipher])
                    result = result ^ int(msg)

                client_result = int(conn.recv(32))
                result_array[i][j] = (result == client_result)
                if(result_array[i][j] == True):
                    print("Adding {} to intersection!".format(numbers[i]))
                    intersection.add(numbers[i])
                conn.send(str(result).encode('utf-8'))
        print(result_array)
    print("Intersection is = ")
    print(intersection)
    print("Number of OT Receivers = {}".format(count_ot))
    receiver_s.close()

def main():
    if(len(argv) != 3):
        print("Usage: python3 driver.py <filename1> <num-buckets>");
        exit

    num_b = int(argv[2])

    test1 = RH.fileReaderAndHash(argv[1],num_b)
    buckets = test1.load_buckets()
    ot_receiver_test(4444, buckets)
    #cProfile.runctx('ot_receiver_test(4444, buckets)',locals(),globals())

if __name__ == "__main__":
    main()