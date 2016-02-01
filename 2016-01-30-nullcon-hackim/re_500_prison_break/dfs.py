from graphviz import Digraph
import os

lines=open("dfs_in").read().split("\n")

neighbours={}

for line in lines:
    if line.strip()=="":
        continue
    line=line.strip()
    spl=line.split(" ")
    fr=int(spl[0], 16)
    i=1
    neighbours[fr]=[]
    while i<len(spl):
        neighbours[fr].append(int(spl[i], 16))
        i+=1

to_add=[]
for vert in neighbours:
    for nei in neighbours[vert]:
        if nei not in neighbours:
            to_add.append(nei)
print "Need to add:"
print [hex(c) for c in to_add]
print "==="
for nei in to_add:
    neighbours[nei]=[] # fails


start=0x77ba4e4b
end=0x4a1b647b
end=0x350f8745
end=0x5bfaa5bf

can_get_from={}
def dfs(pos):
    for n in neighbours[pos]:
        if n not in can_get_from:
            can_get_from[n]=pos
            dfs(n)

def trace(pos):
    if pos==start:
        print hex(start)
    else:
        trace(can_get_from[pos])
        print hex(pos)


#dfs(start)
#print "Can get from:"
#for i in can_get_from:
#    print hex(i),"from",hex(can_get_from[i])
#
#trace(end)
#print bfs(start, end)

states=open("states").read().split("===")[:-1]
ss={}
for state in states:
    if state[0]=="\n":
        state=state[1:]
    print state
    num=int(state.split("\n")[0].split("0x")[1],16)
    rest="\n".join(state.split("\n")[1:])
    ss[num]=rest
ss[0]="NOPE"

dot=Digraph()

for i in neighbours:
    dot.node(hex(i), "STATE "+hex(i)+"\n"+ss[i])

for i in neighbours:
    for e in neighbours[i]:
        dot.edge(hex(i),hex(e))

open("dottest.gv","w").write(dot.source)
dot.render("dottest.gv", view=True)
