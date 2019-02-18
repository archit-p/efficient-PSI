import sys
import encrypt
from fastecdsa import keys,curve, ecdsa
import socket

class Sender():
    def __init__(self, msg1, msg2, srv_port):
        self.a = keys.gen_private_key(curve.P256)
        self.A = keys.get_public_key(self.a,curve.P256)  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv_port = srv_port
        self.msg1 = msg1
        self.msg2 = msg2

    def send_A(self):
        self.sock.connect(('127.0.0.1', self.srv_port))
        ka = keys.export_key(self.A, curve.P256)
        self.sock.send(ka.encode('ASCII'))
        data = self.sock.recv(1024)
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
        data = self.sock.recv(1024)
        print(data)
        self.sock.send(e1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ot_alice.py <port-no>")
    port = sys.argv[1]
    alice = Sender("Nisarg", "Deepak", int(port))
    alice.send_A()

if __name__ == '__main__':
    main()