a="5d0662681e09446e1833653435413f1229".decode('hex')
a=a[0:12]+chr(ord(a[12])^ord(' ')^ord('9'))+a[13:]
a=a[0:13]+chr(ord(a[13])^ord('1')^ord('9'))+a[14:]
a=a[0:14]+chr(ord(a[14])^ord('0')^ord('9'))+a[15:]
a=a[0:15]+chr(ord(a[15])^ord('0')^ord('9'))+a[16:]
a=a[0:16]+chr(ord(a[16])^ord('0')^ord('9'))
print a.encode("hex") 
