from pwn import *
import hashlib
import itertools

r=remote("bringthenoise.insomnihack.ch", 1111)
ln=r.recvline()
chall=ln[-6:-1]
print "Challenge:",chall

i=0
while True:
    if i%200000==0:
        print i,"iterations done..."
    i=i+1
    response=str(i)
    if hashlib.md5(response).hexdigest().strip()[:5]==chall:
        break
print "Found collision:", response

r.sendline(response)

eqs=[]
for i in range(40):
    ln=r.recvline()
    eqs.append([int(x) for x in ln.strip().split(",")])

print "Equations:",eqs

best_err=100000000000
best_sol=[-1]

for sol in itertools.product(range(8), repeat=6):
    err=0
    for i in eqs:
        sm=0
        for j in range(len(i)-1):
            sm=sm+i[j]*sol[j]
        sm=sm%8
        err=err+(abs(i[-1]-sm)+8)%8
    if err<best_err:
        best_err=err
        best_sol=sol
        print "New best sol:",best_sol,best_err

print "Best bet:",best_sol
r.sendline(", ".join([str(x) for x in best_sol]))
r.interactive()
