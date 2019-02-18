import sys
import encrypt
from fastecdsa import keys,curve,ecdsa
import socket

class Receiver():
    def __init__(self, srv_port):
        self.b = keys.gen_private_key(curve.P256)
        self.B = keys.get_public_key(self.b,curve.P256)
        self.port = srv_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_B(self, A):
        c = int(input('Enter the choice bit:'))
        if c==0:
	        print('choice is '+ str(c))
        if c==1:
            print('choice is '+ str(c))
            self.B = self.B + A
    
    def send_B(self):
        e0 = ''
        e1 = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by OT Client', addr)
                data = conn.recv(1024)
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
        self.sock.close()
        kr = A*self.b
        key_hashed_r = encrypt.getHash(str(kr).encode("utf-8"))

        m0 = encrypt.decipher(key_hashed_r,e0)
        m1 = encrypt.decipher(key_hashed_r,e1)

        print(m0)
        print(m1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ot_bob.py <port-no>")
    port = sys.argv[1]
    bob = Receiver(int(port))
    bob.send_B()

if __name__ == '__main__':
    main()
