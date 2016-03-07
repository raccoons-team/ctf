#!/usr/bin/env python
def to_bits(length, N):
  return [int(i) for i in bin(N)[2:].zfill(length)]

def from_bits(N):
  return int("".join(str(i) for i in N), 2)

CRC_POLY = to_bits(65, (2**64) + 0xeff67c77d13835f7)
CONST = to_bits(64, 0xabaddeadbeef1dea)

def crc(mesg):
  mesg += CONST
  shift = 0
  while shift < len(mesg) - 64:
    if mesg[shift]:
      for i in range(65):
        mesg[shift + i] ^= CRC_POLY[i]
    shift += 1
  return mesg[-64:]

def crc_step(mesg,j):
    if mesg[j]:
      for i in range(65):
        mesg[j+i] ^= CRC_POLY[i]
    return mesg

INNER = to_bits(8, 0x36) * 8
OUTER = to_bits(8, 0x5c) * 8

def xor(x, y):
  return [g ^ h for (g, h) in zip(x, y)]

def hmac(h, key, mesg):
  return h(xor(key, OUTER) + h(xor(key, INNER) + mesg))

PLAIN_1 = "zupe zecret"
PLAIN_2 = "BKPCTF"

def str_to_bits(s):
  return [b for i in s for b in to_bits(8, ord(i))]

def bits_to_hex(b):
  return hex(from_bits(b)).rstrip("L")

if __name__ == "__main__":
  with open("key.txt") as f:
    KEY = to_bits(64, int(f.read().strip("\n"), 16))
  print PLAIN_1, "=>", bits_to_hex(hmac(crc, KEY, str_to_bits(PLAIN_1)))
  print "BKPCTF{" + bits_to_hex(hmac(crc, KEY, str_to_bits(PLAIN_2))) + "}"
 
A=[] #[64x64]
Y=[] #[64]

for i in range(64):
  b1=hmac(crc, KEY, str_to_bits(PLAIN_1))
  KEY[63-i]^=1
  b2=hmac(crc, KEY, str_to_bits(PLAIN_1))
  KEY[63-i]^=1
  x= xor(b1,b2)
  
  #test if crc is really linear
  KEY[10]^=1
  b1=hmac(crc, KEY, str_to_bits(PLAIN_1))
  KEY[63-i]^=1
  b2=hmac(crc, KEY, str_to_bits(PLAIN_1))
  x2= xor(b1,b2)
  KEY[63-i]^=1  
    
  if x==x2:
    pass
  else:
    print "test not passed!!!!!!!!!"
    exit(3)
  
  A.append(x)
  Y.append(2**i)
  
#I've got equation [64x64]=[64]

def swap_column(A,Y,a,b):
  tmp=A[a]
  A[a]=A[b]
  A[b]=tmp
  tmp=Y[a]
  Y[a]=Y[b]
  Y[b]=tmp

def sort(A,Y,from_):
  zmiana=True
  while zmiana:
    zmiana=False
    for j in range(from_+1,64):
      if A[j][from_]>A[j-1][from_]:
	swap_column(A,Y,j,j-1)
	zmiana=True
  
def xor_column(A,Y,a,b):
  for t in range(64):
    A[a][t]^=A[b][t]
  Y[a]^=Y[b]
 
def xor_if(A,Y,i):
  for j in range(i+1,64):
    if A[j][i]==1:
      #xor column j with column i
      xor_column(A,Y,j,i)
      
def triangle_to_diagonal(A):
  for i in range(62,-1,-1):
    for j in range(i+1,64):
      if A[i][j]==1:
	#i=i^j
	xor_column(A,Y,i,j)

def gauss_jordan(A,Y):
  for i in range(64):
    sort(A,Y,i)
    xor_if(A,Y,i)
  triangle_to_diagonal(A)  
    
#Y=cipher

gauss_jordan(A,Y)

old_cipher=hmac(crc, KEY, str_to_bits(PLAIN_1))
new_cipher=to_bits(64,0xa57d43a032feb286)

diff=xor(old_cipher,new_cipher)

new_key=from_bits(KEY)

for i in range(64):
  if diff[i]==1:
    new_key^=Y[i]
    
print "KEY"
print hex(new_key)
    
print "TEST"
print hex(0xa57d43a032feb286)+" == "+hex(from_bits(hmac(crc, to_bits(64,new_key), str_to_bits(PLAIN_1))))+ "???"
print "........"

print "flag"
print "BKPCTF{" + bits_to_hex(hmac(crc, to_bits(64,new_key), str_to_bits(PLAIN_2))) + "}"