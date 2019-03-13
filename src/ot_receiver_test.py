from ot_receiver import OTReceiver 
import socket
import random
from fastecdsa import keys,curve, ecdsa
import pickle
import encrypt
import time
import cProfile

def ot_receiver_test(num, port):
    result = 0
    receiver_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver_s.bind(('127.0.0.1', port))
    receiver_s.listen()
    print("listening on port " + str(port))
    conn, addr = receiver_s.accept()
    # use bits of the number as choice bits
    print("received connection from " +  str(addr))
    fail_count = 0
    buckets = [[3, 1, 5, 6, 2],[11, 13, 15, 16, 17]]
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
                print(num_cpy)
                result = 0
                #before starting equality send the length of a bucket
                # equality for a given number
                for k in range(0,8):
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
                    intersection.add(numbers[i])
                conn.send(str(result).encode('utf-8'))
        print(result_array)

    print("Intersection is = ")
    print(intersection)
    receiver_s.close()

def main():
    stime = time.time()
    cProfile.run('ot_receiver_test(10, 4444)')

if __name__ == "__main__":
    main()