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
    
    def send(self):
        e0 = ''
        e1 = ''
        conn, self.addr = self.sock.accept()
        with conn:
            data = conn.recv(177)
            with open('receiver.dat', 'w') as f:
                f.write(data.decode('ASCII'))
            A = keys.import_key('receiver.dat')[1]
            self.set_B(A)
            # send B
            bk = keys.export_key(self.B, curve.P256)
            conn.sendall(bk.encode('ASCII'))
            # recv e0 and e1
            data = conn.recv(1024)
            e0 = data
            conn.sendall(b'Received e0. Send e1.')
            data = conn.recv(1024)
            e1 = data
        kr = A*self.b
        key_hashed_r = encrypt.getHash(str(kr).encode("utf-8"))

        m = list()
        m.append(encrypt.decipher(key_hashed_r,e0))
        m.append(encrypt.decipher(key_hashed_r,e1))

        return m[self.bit]