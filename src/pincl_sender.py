import socket
import sys
sys.path.append('../test/')

from peq_sender import peq_test_sender
from readerHash import fileReaderAndHash


def pincl_test_sender(element, srv_port):
    # connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # while True:
    #     try:
    #         connect_socket.connect(('127.0.0.1', srv_port))
    #     except:
    #         print("Sender stopped comparison")
    #         connect_socket.close()
    #         break
    #     connect_socket.close()
    for index in range(6):
        print("checking element index ", index)
        peq_test_sender(element, srv_port)


def main():
    element = 4
    pincl_test_sender(element, 4444)

if __name__ == "__main__":
    main()