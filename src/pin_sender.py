import sys
import encrypt
from fastecdsa import keys, curve, ecdsa
import socket
import copy
import random


class Sender:
    def __init__(self, srv_port, numberList):
        self.a = keys.gen_private_key(curve.P256)
        self.A = keys.get_public_key(self.a, curve.P256)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv_port = srv_port
        self.numberList = numberList
        self.bitNumList = list()
        for number in self.numberList:
            self.bitNumList.append(self.extendBin(number, 10))

    def xor(self, c1, c2):

        # xors the bits and returns a str
        c1 = int(c1)
        c2 = int(c2)

        return str(c1^c2)

    def extendBin(self, number, finalLen):

        # Returns a list of bits in the number
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

    def send_A(self):

        # Do this multiple times. Receiver sending the B because it depends on the choice bits
        kB = self.sock.recv(1024)
        with open('sender.dat', 'w') as f:
            f.write(kB.decode('ASCII'))
        B = keys.import_key('sender.dat')[1]

        k0 = B*self.a
        k1 = B*self.a - self.A*self.a

        key_hashed_0 = encrypt.getHash(str(k0).encode("utf-8"))
        key_hashed_1 = encrypt.getHash(str(k1).encode("utf-8"))

        # encrypt using k0 and k1
        msg1 = random.randint(0, 2 ** 15 - 1)
        msg2 = random.randint(0, 2 ** 15 - 1)

        msg1 = self.extendBin(msg1, 15)
        msg2 = self.extendBin(msg2, 15)

        e0 = encrypt.cipher(key_hashed_0, self.bitToString(msg1))
        e1 = encrypt.cipher(key_hashed_1, self.bitToString(msg2))

        # send e0 and e1
        self.sock.send(e0)
        data = self.sock.recv(1024)
        print(data)
        self.sock.send(e1)

        return [msg1, msg2]

    def send_A_loop(self):

        self.sock.connect(('127.0.0.1', self.srv_port))
        # Sender sending the A to receiver. Do only once
        kA = keys.export_key(self.A, curve.P256)
        self.sock.send(kA.encode('ASCII'))

        stringArr = list()
        for i in range(0, len(self.bitNumList[0])):
            stringArr.append(self.send_A())

        stringArrSet = list()
        for bitNum in self.bitNumList:
            tempList = []
            for i, bit in enumerate(bitNum):
                tempList.append(stringArr[i][bit])
            stringArrSet.append(tempList)

        finalList = list()

        for stringArr in stringArrSet:
            for i in range(0, 15):
                for j in range(0, len(stringArr)):
                    stringArr[0][i] = self.xor(stringArr[0][i], stringArr[j][i])
            finalList.append(stringArr[0])

        # self.sock.send(self.bitToString(stringArr[0]).encode())
        return finalList


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ot_alice.py <port-no>")
    port = sys.argv[1]
    alice = Sender(int(port), [20, 200])
    print(alice.send_A_loop())


if __name__ == '__main__':
    main()