data={}

trans={ "RSPI_GPIO_7.txt"  : "rs",
        "RSPI_GPIO_8.txt"  : "e",
        "RSPI_GPIO_18.txt" : "d4",
        "RSPI_GPIO_23.txt" : "d5",
        "RSPI_GPIO_24.txt" : "d6",
        "RSPI_GPIO_25.txt" : "d7"}

for filename in trans.keys():
    f=open(filename)

    l1=f.readline().strip().split(" ")
    l2=f.readline().strip().split(" ")

    for i in range(len(l1)):
        b=0
        if float(l2[i])>0.5:
            b=1
        data[float(l1[i])]=(filename, b)



states={"rs":0, "e":0, "d4":0, "d5":0, "d6":0, "d7":0}


bl=False
pr=0
output=""
def outNibble(nib, really=True):
    global bl, pr, output
    if bl==False:
        pr=nib
        bl=True
    else:
        bl=False
        pr=pr*16+nib
        if really==False:
            if pr&128:
                print "Set DDRAM to: ", hex(pr&127)
            elif pr==1:
                print "Clear screen"
            else:
                print "Unknown control sequence"
            output=""
        else:
            output=output+chr(pr)
            print output
        pr=0

for i in sorted(data):
    pin=trans[data[i][0]]
    newstate=data[i][1]
    if states[pin]==newstate:
        continue
    states[pin]=newstate
    if pin=="e":
        if newstate==0:
            if states["rs"]==1:
                outNibble(states["d4"]*8+states["d5"]*4+2*states["d6"]+states["d7"])
            else:
                outNibble(states["d4"]*8+states["d5"]*4+2*states["d6"]+states["d7"], False)

print output
