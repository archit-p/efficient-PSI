from ot_receiver import OTReceiver 
import socket
import random

def peq_test_receiver(num, port):
    result = 0
    receiver_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver_s.bind(('127.0.0.1', port))
    receiver_s.listen()
    print("listening on port " + str(port))

    # use bits of the number as choice bits
    for i in range(0,32):
        bit = num&1
        num = num >> 1
        obj = OTReceiver(bit, receiver_s)
        msg = obj.send()
        print(obj)
        # take xor of previous result and the current message
        result = result ^ int(msg)
    receiver_s.close()
    return result

def main():
    r = peq_test_receiver(10, 4444)
    print(r)

if __name__ == "__main__":
    main()
