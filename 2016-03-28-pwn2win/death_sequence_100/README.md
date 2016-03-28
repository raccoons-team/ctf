# Writeup for Death Sequence (Algorithms 100)

This challenge was about following sequence:
> 1, 1, 1, 1, 10, 46, 217, 1027, 4861, 23005, ...

Our task was to determine last 9 digits of nth element of the sequence and last 9 digits of sum of n first elements.
The main difficulty of this task was that n could be even 
10^18. It is worth to mention, than we are counting positions from 1, not from zero (following task's description).

Firstly we managed to write formula for our sequence:
>f(x) = 1, for x in in range [1,4] (inclusive)  
>f(x) = 10, for x = 5   
>f(x) = 5*f(x-1)-f(x-2)-f(x-3)-f(x-4)-f(x-5)

Another helpful observation is:
>Let name sum(x) that sum(x) = f(1)+f(2)+...+f(n), now:  
>sum(1) = 1      
>sum(2) = 2   
>sum(3) = 3   
>sum(4) = 4   
>sum(5) = 14  
>sum(x) = 5*sum(x-1)-sum(x-2)-sum(x-3)-sum(x-4)-sum(x-5), for x > 5

Now we have to face the problem of very large n.
We can't simply calculate f(x) and sum(n) in linear time.
[Here](http://fusharblog.com/solving-linear-recurrence-for-programming-contest/) is an article about very useful technique which allows us to calculate such information in log(n) time.

I will try to explain this algorithm shortly, but if you want to fully understand it, it would be better to read this article.

So, we created two 6x6 matrices, one for nth element and one for sum:
``` python
baseMatrix = [[ 5,  -1,  -1,  -1,  -1, 10],
	[ 1,  0,  0,  0,  0,  1],
	[ 0,  1,  0,  0,  0,  1],
	[ 0,  0,  1,  0,  0,  1],
	[ 0,  0,  0,  1,  0,  1],
	[ 0,  0,  0,  0,  0,  0]]

baseMatrixSum = [[ 5,  -1,  -1,  -1,  -1, 14],
  [ 1,  0,  0,  0,  0,  4],
  [ 0,  1,  0,  0,  0,  3],
  [ 0,  0,  1,  0,  0,  2],
  [ 0,  0,  0,  1,  0,  1],
  [ 0,  0,  0,  0,  0,  0]]
```

Now if we calculate ```pow(baseMatrix, n)```, the nth number of sequence will be present in ```pow(baseMatrix, n)[0][5]``` and ```pow(baseMatrixSum, n)``` will give us sum of first n elements in ```pow(baseMatrixSum, n)[0][5]```

The operation of ```pow(a, n)``` can be calculated in log(n) time.
Code for ```pow(int a, int n)``` (it works same for matrix, except you have another multiplication operator):
```c++
int pow(int a, int n){
    if(n==0)return 1;
    if(n==1)return a;
    if(n%2==0){
        int tmp = pow(a, n/2);
        return tmp*tmp;
    }
    return pow(a, n-1)*a;
}
```

Unfortunately resulting numbers can still be very large, but all we want are last 9 digist, so we can calculate everything modulo.

Finally, the code - it is made of two pieces, one for connecting with server and another one for calculating sequences (this approach was useful because during the contest we've tried several implementations of sequence part). Both are in python 2.7:
```python
#server part
import socket
import ssl
import subprocess
import time
#openssl s_client -connect programming.pwn2win.party:9001

HOST = "programming.pwn2win.party"
PORT = 9001

HOST = socket.getaddrinfo(HOST, PORT)[0][4][0]
print(HOST)

sock = socket.socket()
sock.connect((HOST, PORT))

sock = ssl.wrap_socket(sock,cert_reqs=ssl.CERT_NONE)

ctr=0
while 1:
	#time.sleep(0.1)
	serv = sock.read();
	print "from server: " + serv.rstrip()
	if serv.startswith("WRONG"):
		break
	proc = subprocess.Popen(["python py_seq.py " + serv], stdout=subprocess.PIPE, shell=True)
	(ans, err) = proc.communicate()
	print "sending " + ans.rstrip() + " as result"
	sock.write(ans)
	ctr+=1
print "finished after " + str(ctr) + " steps"
```

```python
#sequence part
from copy import deepcopy
import sys

baseMatrix = [[ 5,  -1,  -1,  -1,  -1, 10],
	[ 1,  0,  0,  0,  0,  1],
	[ 0,  1,  0,  0,  0,  1],
	[ 0,  0,  1,  0,  0,  1],
	[ 0,  0,  0,  1,  0,  1],
	[ 0,  0,  0,  0,  0,  0]]

baseMatrixSum = [[ 5,  -1,  -1,  -1,  -1, 14],
    [ 1,  0,  0,  0,  0,  4],
    [ 0,  1,  0,  0,  0,  3],
    [ 0,  0,  1,  0,  0,  2],
    [ 0,  0,  0,  1,  0,  1],
    [ 0,  0,  0,  0,  0,  0]]

identityMatrix = [[ 1,  0,  0,  0,  0, 0],
    [ 0,  1,  0,  0,  0,  0],
    [ 0,  0,  1,  0,  0,  0],
    [ 0,  0,  0,  1,  0,  0],
    [ 0,  0,  0,  0,  1,  0],
    [ 0,  0,  0,  0,  0,  1]]

emptyMatrix = [[ 0,  0,  0,  0,  0, 0],
    [ 0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0],
	[ 0,  0,  0,  0,  0,  0]]

def dispMatrix(m):
	for i in range(0,6):
		toDisp=""
		for j in range(0,6):
			toDisp += str(m[i][j])
			toDisp += " "
		print toDisp

def multiMod(left, right, mod):
	retVal = deepcopy(emptyMatrix)
	tmpMod = 1000000000000
	for i in range(0,6):
		for j in range(0,6):
			retVal[i][j]=0
			for k in range(0,6):
				retVal[i][j] += (left[i][k])*(right[k][j])
				retVal[i][j] %= tmpMod
	return retVal

def powerModulo(m, n, mod):
	if n == 0:
		return deepcopy(identityMatrix) 
	if n == 1:
		return deepcopy(m)
	if n % 2 == 0:
		tmp = powerModulo(m, n/2, mod)
		return multiMod(tmp, tmp, mod)
	return multiMod(powerModulo(m, n-1, mod), m, mod)

modNum = 1000000000
inputFromServ = long(sys.argv[1])-4
matrixA = powerModulo(baseMatrix, inputFromServ, 1000000000000000)
matrixB = powerModulo(baseMatrixSum, inputFromServ, 1000000000000000)

str1 = str(matrixA[0][5]%modNum)
str1 = '0'*(9-len(str1)) + str1
str2 = str(matrixB[0][5]%modNum)
str2 = '0'*(9-len(str2)) + str2
print str1+" "+str2
```

And after a while we were given a flag:
>CTF-BR{It-wAs-jUsT-a-ReCURsIVe-SequenCE-to-BE-coded-In-LOGN-XwmIBVyZ5QEC}