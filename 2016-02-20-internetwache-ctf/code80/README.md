 # Internetwache CTF 2016: Brute with Force (code 80)  
  

>Description: People say, you’re good at brute forcing… Have fun! Hint: You don’t need to crack the 31. character (newline). Try to think of different (common) time representations.   
Service: 188.166.133.53:11117

Like with box of chocolates - you never know what to expect until you taste. So lets taste this adress with `nc 188.166.133.53 11117`

We are getting smth like that:
```
People say, you're good at brute forcing...  
Hint: Format is TIME:CHAR"
'Char 0: Time is 22:43:41, 051th day of 2016 +- 30 seconds and the hash is: 0834c5dd70c8741520918d6093310ad5c1a20f1d'
```

At first glance this hash can be MD5 or SHA, lets check length:
`expr length "0834c5dd70c8741520918d6093310ad5c1a20f1d"`  
`result: 40`

So big chance its *SHA1*.  
Now looking at hint: `Hint: Format is TIME:CHAR"` seems that we need to enter something like `<time in specific format>:<current char from flag>`.  

This information about time: `051th day of 2016 +- 30 seconds` suggested its about *epoch time* . I also know that flag starts from `IW{`.Ok, I always wanted to learn coding in Python, so seems like good ocasion for it. I generated some hashes in time around server time:

```
epoch = int(time.time())

for i in range(-3000, 3000):
    print "Current %d" % (i)
    hash_object = hashlib.sha1(str(epoch+i)+":I")
    hex_dig = hash_object.hexdigest()
    print(hex_dig)
```

I've checked them with `grep` - and got it. Hash from server response was there. I adjusted time in script, an automated it for next two letters of flag `W{`.

Next letter is unknown, and it where bruteforcing gets usefull. For each next response from server I was generatting hashes like `sha1(<epoch_time>:<next_letter_from_dictionary>)` in timespan `-300,+300` and comparing them. If hash was found - I had new letter and could send response to server. After script execution I have flag.

```
import calendar
import time
import hashlib
import datetime
import socket

print "start"

dictionary="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789_{}-+-*!@#$%^&"


def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    
    #s.shutdown(socket.SHUT_WR)
    i=0
    while 1:
        data = s.recv(1024)
        epoch = epoch_time = int(time.time())+4*60+20  #I have different time locally than server, so needed to adjust that
	#print "epoch_new " + str(epoch)
        if data == "":
            break
	#print str(i)+"Received:", repr(data)
        if "hash" in data:
	  print "matched "+data.split(" ")[-1].strip()+"#"        
        
        if (i>=1):
	  answer=check(data,i,epoch)
	  print "sending "+answer
	  s.sendall(answer)
	  time.sleep(2) #I wanted to make sure that I'll be generating new hash for different timestamp
        i=i+1
    print "Connection closed."
    s.close()



def check(xx,idx,epoch):
  print "Function check" 
  index = xx.split(' ')
  hash = index[-1]
  hash=hash.strip()
  asci=""
  
  if idx==1:
    asci=":I"
  if idx==2:
    asci=":W"
  if idx==3:
    asci=":{"
  
  #We know first three letters of flag, as format is IW{
  if (idx <= 3):
    for i in range(-300, 300):
      hash_object = hashlib.sha1(str(epoch+i)+asci)
      hex_dig = hash_object.hexdigest()
      if hex_dig == hash:
	print "gotcha: "+hash+" "+str(epoch+i)+asci
	return str(epoch+i)+asci
  
  #We have to bruteforce each sign, from forth letter, until script fails
  if (idx >=4):
      for c in dictionary:
	asci=":"+str(c)
	for i in range(-300, 300):
	  hash_object = hashlib.sha1(str(epoch+i)+asci)
	  hex_dig = hash_object.hexdigest()
	  if hex_dig == hash:
	    print "gotcha: "+hash+" "+str(epoch+i)+asci
	    return str(epoch+i)+asci


netcat("188.166.133.53",11117,"")
print "end"
```
**Flag: IW{M4N_Y0U_C4N_B3_BF_M4T3RiAL!}**

