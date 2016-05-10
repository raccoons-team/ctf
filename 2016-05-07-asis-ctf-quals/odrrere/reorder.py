#!/usr/bin/env python2

import binascii
import struct
import sys

PNG_MAGIC = '89504e470d0a1a0a'.decode('hex')

def chunks(stream):
    while True:
        chk_len_raw = stream.read(4)
        if not chk_len_raw:
            return
        chk_len, = struct.unpack('>I', chk_len_raw)
        chk_type = stream.read(4)
        chk_data = stream.read(chk_len)
        chk_crc_raw = stream.read(4)
        chk_crc, = struct.unpack('>I', chk_crc_raw)
        calc_crc = binascii.crc32(chk_type + chk_data) & 0xffffffff
        if chk_crc != calc_crc:
            print 'CRC32 mismatch :( Expected 0x%08x, got 0x%08x' % (chk_crc, calc_crc)
            exit(2)
        yield chk_type, chk_len + chk_type + chk_data + chk_crc

with open('odrrere', 'rb') as f:
    header = f.read(8)
    if header != PNG_MAGIC:
        print 'Not a valid PNG :('
        exit(1)
    header = [PNG_MAGIC]
    idat = []
    trailer = []
    for t, data in chunks(f):
        if t == 'IDAT':
            idat.append(data)
        elif t == 'IEND':
            trailer.append(data)
        else:
            header.append(data)
    header.append(idat[0])
    header = ''.join(header)
    body = ''.join(idat[int(i)] for i in sys.argv[2:])
    trailer = ''.join(trailer)
    open(sys.argv[1], 'w+b').write(header + body + trailer)
