import string

disas=open("dump").read()

class State(object):
    pass

class Chunk(object):
    pass

machine=[]

chunks={}

def parse_addr(s):
    # 400f0a    jmp    400f0f <SHA1_Update@plt+0x6af>
    s=s[string.find(s,"j"):]
    s=s[string.find(s,"4"):string.find(s,"<")]
    return int(s.strip(),16)


lines=disas.split("\n")
for i in range(985/5):
    # Doing i*5 to i*5+4, eg.
    # 400ed7  mov    eax,DWORD PTR [rbp-0x1b0]
    # 400edd  sub    eax,0x7d408df0
    # 400ee2  mov    DWORD PTR [rbp-0x1b8],eax
    # 400ee8  jg     40240f
    # 400eee  jmp    400ef3
    chunk=Chunk()
    
    chunk.cool=False
    chunk.sub=int(lines[i*5+1].split("eax,0x")[1],16)
    addr1=parse_addr(lines[i*5+3])
    addr2=parse_addr(lines[i*5+4])
    if string.find(lines[i*5+3],"jg")!=-1:
        chunk.jl=addr2
        chunk.je=addr2
        chunk.jg=addr1
    else: # je
        chunk.jl=addr2
        chunk.je=addr1
        chunk.jg=addr2
        chunk.cool=True
    chunks[ int(lines[i*5].split("mov")[0].strip(), 16) ]=chunk

at_addr={}
i=0
for line in lines[:-1]:
    spl=line.split("\t")
    at_addr[int(spl[0], 16)]=(line,i)
    i+=1

final_addresses={}
chunks_as_state={}
for addr in chunks:
    final_addresses[addr]={}
    if chunks[addr].cool:
        final_addresses[addr][chunks[addr].sub]=chunks[addr].je
        i=at_addr[chunks[addr].je][1]
        chunks_as_state[chunks[addr].sub]=""
        #print "STATE #"+hex(chunks[addr].sub)
        while True:
            #print lines[i]
            chunks_as_state[chunks[addr].sub]=chunks_as_state[chunks[addr].sub]+"\n"+lines[i]
            if string.find(lines[i], "jmp")!=-1:
                break
            i+=1
        #print "==="

for a in final_addresses:
    for b in final_addresses[a]:
        pass
        #print "if(glowna_zmienna=="+hex(b)+") goto "+hex(final_addresses[a][b])+";"

states=[0x8c239e00, 0x6604d6c7, 0xdf6f90a3, 0x92ca3194, 0x22891025, 0x47b7d5a2, 0x8ed36736,
        0x4e763eda, 0x4c101bc1, 0x81caba64, 0x9f57a1c0, 0x99c26b82, 0x3b428c51, 0x4bda4dd1,
        0x1d15da90, 0xf022a7a7, 0x9fd9843d, 0xe971bdc4, 0xfb808397, 0xddc1cdad, 0xa6a84318,
        0x3fd168c1,0x7b6c13f9, 0xe89d1a60, 0xac616384, 0x3ccb3966, 0xba0384a3, 0x574b6a09, 0xfcc46220,
        0xa60c2a30, 0x1941ebee, 0xd480a297, 0x350f8745]
for s in states:
    print "=== chunk "+hex(s)+" ==="
    print chunks_as_state[s]
    print "==="
