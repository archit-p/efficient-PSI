import sys
import encrypt
from fastecdsa import keys,curve, ecdsa
import socket

class OTSender():
    '''
    Sender connects to a server port and starts sending its data
    msg1 = first message for OT
    msg2 = second message for OT
    srv_port = port on which server is running
    sock = socket to communicate
    '''
    def __init__(self, msg1, msg2, srv_port, sock):
        self.a = keys.gen_private_key(curve.P256)
        self.A = keys.get_public_key(self.a,curve.P256)  
        self.sock = sock
        self.srv_port = srv_port
        self.msg1 = msg1
        self.msg2 = msg2
        self.e0 = ''
        self.e1 = ''
        self.k0 = ''
        self.k1 = ''

    def __str__(self):
        return "---------------------\n" + "OT Strings are:\n" + "1. " + self.msg1 + "\n2. " + self.msg2 + "\n---------------------\n"

    def sender_keygen(self, B):
        key0 = B*self.a
        key1 = B*self.a - self.A*self.a
        self.k0 = encrypt.getHash(str(key0).encode("utf-8"))
        self.k1 = encrypt.getHash(str(key1).encode("utf-8"))
        self.e0 = encrypt.cipher(self.k0,self.msg1).decode("utf-8")
        self.e1 = encrypt.cipher(self.k1,self.msg2).decode("utf-8")
        ciphers = {
            "e0": self.e0,
            "e1": self.e1
        }
        return ciphers

    def send(self):
        

        data = self.sock.recv(1024)
