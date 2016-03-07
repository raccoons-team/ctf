# Writeup for hmac_crc CRYPTO (5) 

> We're trying a new mac here at BKP---HMAC-CRC. The hmac (with our key) of "zupe zecret" is '0xa57d43a032feb286'.  What's the hmac of "BKPCTF"? https://s3.amazonaws.com/bostonkeyparty/2016/0c7433675c3c555afb77271d6a549bf5d941d2ab

original script can be downloaded below

![0c7433675c3c555afb77271d6a549bf5d941d2ab](0c7433675c3c555afb77271d6a549bf5d941d2ab)

We are given a hmac functions which takes hash function, message and key as input and gives sign of the message  
They give us the message and sign of this message using unknown key and we are supposed to sign another given message using the same key  

code of signing function:

```python
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

INNER = to_bits(8, 0x36) * 8
OUTER = to_bits(8, 0x5c) * 8

def hmac(h, key, mesg):
  return h(xor(key, OUTER) + h(xor(key, INNER) + mesg))
```

I was thinking about this algorithm and I came to the conclusion that when we flip one bit in key, all bits of the output depending on this bit also flip with no matter of other bits in key  

another words when we have a message msg and two different keys: key1 and key2  

	hmac(h,key1,msg) xor hmac(h,key1 with flipped bit x)  =  hmac(h,key2,msg) xor hmac(h,key2 with flipped bit x)  

this means that hmac is linear  

We can gather all positions of changed bits in sign when bit at position x in key will change for the given message  

I used gauss-jordan algorithm to compute which bits in key need to flip if I want flip one bit in sign at given position  

I created my own pair key,sign for given message and I was looking which bits are different  

when some bit was different I xored my key with bits I computed using gauss-jordan and I got needed key  

my code is below  

![crypto1.py](crypto1.py)

put to file key.txt some 8B hex digit without '0x'

