from pwn import *
import zlib, binascii, bz2, subprocess

r=remote("52.91.163.151",30303)
context.log_level="DEBUG"

def recv_score():
    r.recvregex("Current Score :\d+/25")

def decode(s):
    s=s.strip()
    print "Decoding: ",repr(s)
    if string.find(s, "ba64-")==0:
        return base64.b64decode(s[5:])
    if string.find(s, "revs-")==0:
        return (s[-1:4:-1])
    if string.find(s, "zlib-")==0:
        return zlib.decompress(s[5:])
    if string.find(s, "ba16-")==0:
        return binascii.unhexlify(s[5:])
    if string.find(s, "ba32-")==0:
        return base64.b32decode(s[5:])
    if string.find(s, "hexa-")==0:
        return binascii.unhexlify(s[5:])
    if string.find(s, "ro42-")==0:
        ss=s[5:]
        if ss=="buqtrou":
            return "Lead bye"
        if ss=="yvoekjho":
            return "If you try"
        if s[5:]=="oekhweqbi":
            return "Your goals"
        if s[5:]=="tedejmyixyj":
            return "Do not wish it"
        if s[5:8]=="yjy":
            return "It is better"
        if s[5]=="y":
            return "If at first"
        if s[5]=="b":
            return "Luck is"
        if s[5]=="j":
            return "Thank you"
        return "Very little"
    if string.find(s, "roti-")==0:
        return s[5:].decode("rot_13")
    if string.find(s, "ebcd-")==0:
        return s[5:].decode("EBCDIC-CP-BE")
    if string.find(s, "bfuk-")==0:
        open("/tmp/asd","w").write(s[5:])
        return subprocess.check_output(["bf", "/tmp/asd"])
    if string.find(s, "bz2c-")==0:
        return bz2.BZ2Decompressor().decompress(s[5:])
    if string.find(s, "bina-")==0:
        return ''.join(chr(int(s[i+5:i+8+5], 2)) for i in xrange(0, len(s[5:]), 8))


recv_score()

while True:
    sleep(0.2);
    s=r.recv()
    r.send(decode(s))
    recv_score()
