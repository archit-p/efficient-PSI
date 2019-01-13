import sys
sys.path.append('/simplest-oblivious-transfer-master/src')
import encrypt
from fastecdsa import keys,curve, ecdsa

msg1 = "This is Deepak K"
msg2 = "This is Nisarg Joshi"


## The private key of Alice. Corresponds to 'a' in the prime group DH
a = keys.gen_private_key(curve.P256)

## The public key of Alice to be shared with Bob. Corresponds to 'g^a'
A = keys.get_public_key(a,curve.P256)


## The private key of Bob. Corresponds to 'b' in the prime group DH
b = keys.gen_private_key(curve.P256)

## The public key of Bob to be shared with Alice. Corresponds to 'g^b'
B = keys.get_public_key(b,curve.P256)


## Based on value of choice bit c
## let c = 0 then B = g^b which is the value of public key of Bob
## let c = 1 then B = A.g^b in prime group, so in ECC it is (current value of) B + A (Point addition)

c = int(input('Enter the choice bit:'))

if c==0:
	print('choice is '+ str(c))

if c==1:
	print('choice is '+ str(c))
	B = B + A


# Keys computed by Alice based on value of B sent by Bob
k0 = B*a
k1 = B*a - A*a

# print(k0.x)
# print(k1.x)

# Computed by Bob
kr = A*b

key_hashed_0 = encrypt.getHash(str(k0).encode("utf-8"))
key_hashed_1 = encrypt.getHash(str(k1).encode("utf-8"))
key_hashed_r = encrypt.getHash(str(kr).encode("utf-8"))

print(key_hashed_0)
print(key_hashed_1)
print(key_hashed_1)

# print(hex(k0.x))
# print(hex(k1.x))
# print(hex(kr.x))

e0 = encrypt.cipher(key_hashed_0,msg1)
e1 = encrypt.cipher(key_hashed_1,msg2)
m0 = encrypt.decipher(key_hashed_r,e0)
m1 = encrypt.decipher(key_hashed_r,e1)

print(m0)
print(m1)