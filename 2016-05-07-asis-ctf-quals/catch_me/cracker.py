flag="\x87\x29\x34\xc5\x55\xb0\xc2\x2d\xee\x60\x34\xd4\x55\xee\x80\x7c\xee\x2f\x37\x96\x3d\xeb\x9c\x79\xee\x2c\x33\x95\x78\xed\xc1\x2b";
 
def valid(c):
  c=chr(c)
  if c>='0' and c<='9':
    return True
  if c>='a' and c<='z':
    return True
  if c>='A' and c<='Z':
    return True
  if c=='-':
    return True
  if c=='_':
    return True
  return False

l=[[],[],[],[],[],[],[],[]]
 
def brut(i):
  global l
  for c in range(0,256):
    ch1=c^ord(flag[i])
    ch2=c^ord(flag[i+8])
    ch3=c^ord(flag[i+16])
    ch4=c^ord(flag[i+24])
    
    if valid(ch1) and valid(ch2) and valid(ch3) and valid(ch4):
      print "position: "+str(i)+" - "+hex(c)
      l[i].append(chr(c))
      #print l
      

for i in range(8):
  brut(i)
  
p=0
for i in l:
  print "position:"+str(p)
  print "length:"+str(len("".join(i)))
  print repr("".join(i))
  p=p+1 
