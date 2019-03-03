from ot_sender import OTSender
import socket
import random

def peq_test_sender(num,srv_port):
    str_list = []
    result = 0
    for i in range(0,32):
        bit = num&1
        num = num >> 1
        sender_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rand_str = []
        rand_str.append(str(random.randint(10000000,20000000)))
        rand_str.append(str(random.randint(10000000,20000000)))
        str_list.append(rand_str[bit])
        obj = OTSender(rand_str[0],rand_str[1],4444,sender_s)
        obj.send()
        print(obj)

    for choice_str in str_list:
        result = result ^ int(choice_str)

    return result

def main():
    s = peq_test_sender(10,4444)
    print(s)

if __name__ == "__main__":
    main()
