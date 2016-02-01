# PrisonBreak

> Break it Free.

We did not have time to finish this task, but we solved a part of it - so we decided to make a 
writeup summarizing what we managed to do.

We were given a binary - typical run:
```
Welcome to the Mini-Prison (not secure, but hard to escape)!!

You should select a cell and find a path to escape to the flag.

You will not be disappointed!!
Select your cell (1-3):1

Go on enter your path:a
s
q
Path Blocked!!
```
So we have to input a number (1-3) and then a sequence of characters. 

Looking at disassembly, we can notice there is one huge loop, consisting in big part of five instructions almost copied
and pasted hundreds of times, such as:
```
  4012e3:       mov    eax,DWORD PTR [rbp-0x1b0]
  4012e9:       sub    eax,0xa72c240a
  4012ee:       mov    DWORD PTR [rbp-0x24c],eax
  4012f4:       jg     40131b
  4012fa:       jmp    4012ff
```

All of those chunks had the same structure:
- mov eax, [rbp-0x1b0]
- sub eax, some_constant
- mov [rbp-some_value], eax
- jg/je some_address
- jmp other_address

So, the pseudocode of the whole binary looked mostly like this (`next_state`-`[rbp-0x198]`, `state`-`[rbp-0x1b0]`):
```
initial instructions;
next_state=0x77ba4e4b;
while(1){
  state=next_state;
  switch(state){
  case 0x111:
    do_stuff1;
    next_state=0x123;
  case 0x234:
    do_stuff2;
    if(condition){
      next_state=0x654;
    }
    else{
      next_state=0x986;
    }
  }
  case 0x987:
    ...
}
```
You get the idea. It was basically a state machine. There were three places, in which the binary writes string
`The flag is nullcon{%s}` - probably one for each initial cell choice. We tried to find a way to get to these states,
however it was very difficult to do it manually. Eventually, we wrote a script which would do it for us - generate an
actual graph with its nodes corresponding to pieces of non-boilerplate code.
