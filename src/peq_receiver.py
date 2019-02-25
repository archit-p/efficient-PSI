import sys
import encrypt
from fastecdsa import keys, curve, ecdsa
import socket


class Receiver:
    def __init__(self, srv_port, number):
        self.b = keys.gen_private_key(curve.P256)
        self.B = keys.get_public_key(self.b, curve.P256)
        self.BCopy = self.B
        self.port = srv_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.number = number
        self.bitNum = self.extendBin(number, 10)

    def xor(self, c1, c2):
        c1 = int(c1)
        c2 = int(c2)

        return str(c1^c2)

    def extendBin(self, number, finalLen):

        bin = lambda n: n > 0 and [n & 1] + bin(n >> 1) or []
        arr = bin(number)

        arr_len = len(arr)

        if arr_len >= finalLen:
            pass
        else:
            for _ in range(finalLen - arr_len):
                arr = [0] + arr

        return arr

    def bitToString(self, msg):

        # Takes an arr of bits and returns a string
        res = ""
        for bit in msg:
            res+=str(bit)

        return res

    def set_B(self, A, c):
        if c == 0:
            print('choice is ' + str(c))
            self.BCopy = self.B
        if c == 1:
            print('choice is ' + str(c))
            self.BCopy = self.B + A

    def send_B_loop(self):

        stringArr = list()
        finalArr = list()

        with self.sock as s:
            s.bind(('127.0.0.1', self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by OT Client', addr)
                data = conn.recv(1024)
                with open('receiver.dat', 'w') as f:
                    f.write(data.decode('ASCII'))
                A = keys.import_key('receiver.dat')[1]

                for i in range(0, len(self.bitNum)):
                    self.set_B(A, self.bitNum[i])
                    bk = keys.export_key(self.BCopy, curve.P256)
                    conn.sendall(bk.encode('ASCII'))

                    data = conn.recv(1024)
                    e0 = data
                    conn.sendall(b'Received e0. Send e1.')
                    data = conn.recv(1024)
                    e1 = data

                    kr = A * self.b
                    key_hashed_r = encrypt.getHash(str(kr).encode("utf-8"))

                    m0 = str(encrypt.decipher(key_hashed_r, e0))
                    m1 = str(encrypt.decipher(key_hashed_r, e1))

                    print(m0)
                    print(m1)

                    if self.bitNum[i] == 0:
                        stringArr.append([int(i) for i in m0])
                    elif self.bitNum[i] == 1:
                        stringArr.append([int(i) for i in m1])

                finalArr = conn.recv(1024)

            # stringArr = self.send_B(conn, A)

            for i in range(0, 15):
                for j in range(0, len(stringArr)):
                    stringArr[0][i] = self.xor(stringArr[0][i], stringArr[j][i])

            if finalArr.decode() == self.bitToString(stringArr[0]):
                print("Equal")
            else:
                print("Unequal")
            return stringArr[0]


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ot_bob.py <port-no>")
    port = sys.argv[1]
    bob = Receiver(int(port), 500)
    print(bob.send_B_loop())


if __name__ == '__main__':
    main()
