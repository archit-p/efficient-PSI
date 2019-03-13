import sys
import encrypt
from fastecdsa import keys,curve,ecdsa
import socket

class OTReceiver():
    def __init__(self, choice, sock):
        self.b = keys.gen_private_key(curve.P256)
        self.B = keys.get_public_key(self.b,curve.P256)
        self.sock = sock
        self.bit = choice
        self.addr = ''

    def __str__(self):
        return "---------------------\n" + "Choice bit = " + str(self.bit) + "\nConnected to client \n" + str(self.addr) + "\n---------------------\n"

    def set_B(self, A):
        if self.bit==1:
            self.B = self.B + A
