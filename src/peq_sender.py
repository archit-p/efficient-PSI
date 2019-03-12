from ot_sender import OTSender
import socket
import random

def peq_test_sender(num,srv_port):
    str_list = []
    result = 0
    # sender_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for _ in range(0,10):
        sender_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("loop in sender")
        bit = num&1
        num = num >> 1
        rand_str = []
        rand_str.append(str(random.randint(10000000,20000000)))
        rand_str.append(str(random.randint(10000000,20000000)))
        str_list.append(rand_str[bit])
        obj = OTSender(rand_str[0],rand_str[1],srv_port,sender_s)
        obj.send()
        # sender_s.close()
        # print(obj)

    # sender_s.close()

    for choice_str in str_list:
        result = result ^ int(choice_str)

    sender_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sender_s.connect(('127.0.0.1', srv_port))

    sender_s.sendall(str(result).encode('ASCII'))
    sender_s.close()

    print(result)

    return result

def main():
    s = peq_test_sender(10,4446)
    print(s)

if __name__ == "__main__":
    main()
