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

    def __str__(self):
        return "---------------------\n" + "OT Strings are:\n" + "1. " + self.msg1 + "\n2. " + self.msg2 + "\n---------------------\n"

    def send(self):
        try:
            self.sock.connect(('127.0.0.1', self.srv_port))
        except:
            print("Could not connect to server. Start server using peq_receiver.py first.")
            exit(1)
            
        ka = keys.export_key(self.A, curve.P256)
        self.sock.send(ka.encode('ASCII'))
        data = self.sock.recv(177)
        with open('sender.dat', 'w') as f:
            f.write(data.decode('ASCII'))
        B = keys.import_key('sender.dat')[1]
        k0 = B*self.a
        k1 = B*self.a - self.A*self.a

        key_hashed_0 = encrypt.getHash(str(k0).encode("utf-8"))
        key_hashed_1 = encrypt.getHash(str(k1).encode("utf-8"))
        # encrypt using k0 and k1
        e0 = encrypt.cipher(key_hashed_0,self.msg1)
        e1 = encrypt.cipher(key_hashed_1,self.msg2)

            # send e0 and e1
        self.sock.send(e0)
        self.sock.send(e1)

        data = self.sock.recv(1024)
