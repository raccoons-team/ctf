# Baby-re (21) writeup

In this challenge we were given a binary file called [baby-re](baby-re). Our goal was to reverse it and find a proper input of 13 integers.

*$./baby-re*
> Var[0]: 1  
  Var[1]: 2   
  Var[2]: 3  
  Var[3]: 4  
  Var[4]: 5  
  Var[5]: 6  
  Var[6]: 7  
  Var[7]: 8  
  Var[8]: 9  
  Var[9]: 10  
  Var[10]: 11  
  Var[11]: 12  
  Var[12]: 13  
  Wrong

We started from:  *$ file baby-re*
> baby-re: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=5d5783d23d78bf70b80d658bccbce365f7448693, not stripped

Then we reversed it using:
[Reverse/PLASMA script](http://github.com/joelpx/plasma).  
We found that there are only two important functions in baby-re binary: `main` and `CheckSolution`.  
(reversed code: [main.reverse](main.reverse) and [CheckSolution.reverse](CheckSolution.reverse))  

All what main does is to read 13 integers with `scanf("%d", &d)`, then it calls `CheckSolution`. Now if our input was proper it will end up printing the numbers in the same order as they were read from input, as chars, which should give the flag. Otherwise it will end with message "Wrong".

So now we need to figure out `CheckSolution`, we can see a following pattern:  
       
``` 
//lots of asm, but nothing interesting
 if (eax != 21399379) {  
      0x401693: jmp 0x401697  
      0x401697: eax = 0  
      0x40169c: jmp 0x4025d1  
 }else 
    //lots of asm, but nothing interesting  
            if (eax != 1453872) {  
            0x4017db: jmp 0x4017df  
            0x4017df: eax = 0  
            0x4017e4: jmp 0x4025d1  
        } else {  
            ... next 11 ifs
        }
```   
`CheckSolution` contains 13 nested `if-else` instructions, every `if` compares value of `eax` with some constant. If comparison is true, then we go to lower-level if, otherwise we will return from `CheckSolution (jmp 0x4025d1 )`:        
```
    0x4025d1: rsi = *(rbp - 8)
    # 0x4025d5: xor rsi, qword ptr fs:[0x28]
    # 0x4025de: je 0x4025e5
    if ((rsi ^= *(fs + 40)) != 0) {
        0x4025e0: call (.plt) __stack_chk_fail
    }
    ret_0x4025e5:
    0x4025e5: leave
    0x4025e6: ret
```        

Next thing to do was to open baby-re in gdb. We put 13 breakpoints in comparisons with constants: `0x000000000040168c <+4038>:	cmp    eax,0x1468753`.  
```
i b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x000000000040168c <CheckSolution+4038>
2       breakpoint     keep y   0x00000000004017d4 <CheckSolution+4366>
3       breakpoint     keep y   0x0000000000401920 <CheckSolution+4698>
4       breakpoint     keep y   0x0000000000401a6b <CheckSolution+5029>
5       breakpoint     keep y   0x0000000000401bb7 <CheckSolution+5361>
6       breakpoint     keep y   0x0000000000401d06 <CheckSolution+5696>
7       breakpoint     keep y   0x0000000000401e52 <CheckSolution+6028>
8       breakpoint     keep y   0x0000000000401fa0 <CheckSolution+6362>
9       breakpoint     keep y   0x00000000004020e8 <CheckSolution+6690>
10      breakpoint     keep y   0x0000000000402234 <CheckSolution+7022>
11      breakpoint     keep y   0x0000000000402378 <CheckSolution+7346>
12      breakpoint     keep y   0x0000000000402499 <CheckSolution+7635>
13      breakpoint     keep y   0x00000000004025ba <CheckSolution+7924>
```

Now i will refer to value of `eax` in first breakpoint as `eax1`, in second breakpoint as `eax2`... in 13 breakpoint as `eax13`.  What we observed, was that for input      

```0,0,...,0,0``` ```eax1=eax2=eax3=...=eax12=eax13=0```.

So we tried with inputs: `1,0,0,...,0,0`, `2,0,0,...,0,0`, `3,0,0,...,0,0`.  
For first input: `eax1=37485`  
For second input: `eax1=74970`  
For third input: `eax1=112455`  
Wait a moment. Isn't it arithmetic progression?
```112455-74970 == 74970-37485 == 37485```
We checked this also for inputs with `1,2,3` in another positions. This also gave us arithmetic progressions (with various differences).  
This looks a bit like a linear equation of 13 variables to solve, so we started writing a python script to solve them, using [Z3Prover python bind](http://github.com/Z3Prover/z3). At this moment we have informations about 1 equation only.  
```
from z3 import *

a   = BitVec('a',32)
b   = BitVec('b',32)
c   = BitVec('c',32)
d   = BitVec('d',32)
e   = BitVec('e',32)
f   = BitVec('f',32)
g   = BitVec('g',32)
h   = BitVec('h',32)
i   = BitVec('i',32)
j   = BitVec('j',32)
k   = BitVec('k',32)
l   = BitVec('l',32)
m   = BitVec('m',32)

s = Solver()
s.add( 37485*a - 21621*b - 1874*c - 46273*d + 50633*e + 43166*f + 29554*g +16388*h + 57693*i + 14626*j + 21090*k + 39342*l + 54757*m == 21399379)
print s.check()
print s.model()
```
>$ python firstEquation.py  
>[b = 0,
 c = 0,
 d = 0,
 e = 0,
 f = 0,
 g = 0,
 h = 0,
 i = 0,
 j = 0,
 k = 0,
 l = 0,
 m = 0,
 a = 2830198975]

> in gdb:  
> run  
> input from firstEquation.py  
> Breakpoint 1, 0x000000000040168c in CheckSolution ()  
> p/x $eax  
> $7 = 0x1468753  

So we found how to pass trough first if!  
To pass trough `eax2` we can repeat previous method:  
> run  
> input -> 1,0,0,..,0,0  
> Breakpoint 1, 0x000000000040168c in CheckSolution ()  
> n  
> set $eflags ^= (1<<6)               //6 -> Zero Flag  
> c  
> p/d $eax  
> $10 = 50936  

Changing 1 to 2 and 3 in input, proves that values of `$eax2` will also form an arithmetic progression with difference 50936.  
This gdb macro automates whole process:  

```
define hack
set $list = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1}
set $i = 0
while($i<13)
	set $list[$i] = $eax
	n
	set $eflags ^= (1<<6)
	c
	set $i = $i+1
end
set $i=0
while($i<13)
	p/d $list[$i]
	set $i = $i+1
end
end
```

Example output of `hack` for input `1,0,0,...,0,0`:  
> $11 = 37485  
  $12 = 50936  
  $13 = -38730  
  $14 = 57747  
  $15 = -14005  
  $16 = -40760  
  $17 = -47499  
  $18 = -65419  
  $19 = 1805  
  $20 = -42941  
  $21 = -37085  
  $22 = 36650  
  $23 = 51735  

All we have to do now is to run baby-re 13 times in gdb, launch our `hack` macro once on every run and then update all 13 equations in z3 script.  

This gives us following script:  
```
from z3 import *

a	= BitVec('a',32)
b	= BitVec('b',32)
c	= BitVec('c',32)
d	= BitVec('d',32)
e	= BitVec('e',32)
f	= BitVec('f',32)
g	= BitVec('g',32)
h	= BitVec('h',32)
i	= BitVec('i',32)
j	= BitVec('j',32)
k 	= BitVec('k',32)
l	= BitVec('l',32)
m	= BitVec('m',32)

s = Solver()
s.add( 37485*a - 21621*b - 1874*c - 46273*d + 50633*e + 43166*f + 29554*g +16388*h + 57693*i + 14626*j + 21090*k + 39342*l + 54757*m == 21399379)
s.add( 50936*a +  4809*b - 6019*c + 38962*d + 14794*e + 22599*f +  -837*g -36727*h - 50592*i - 11829*j - 20046*k + -9256*l + 53228*m == 1453872)
s.add(-38730*a + 52943*b -16882*c + 26907*d - 44446*e - 18601*f - 65221*g -47543*h + 17702*i - 33910*j + 42654*k +  5371*l + 11469*m == -5074020)
s.add( 57747*a - 23889*b -26016*c - 25170*d + 54317*e - 32337*f + 10649*g +34805*h -  9171*i - 22855*j +  8621*k -   634*l - 11864*m == -5467933)
s.add(-14005*a + 16323*b +43964*c + 34670*d + 54889*e -  6141*f - 35427*g -61977*h + 28134*i + 43186*j - 59676*k + 15578*l + 50082*m == 7787144)
s.add(-40760*a - 22014*b +13608*c -  4946*d - 26750*e - 31708*f + 39603*g +13602*h - 59055*i - 32738*j + 29341*k + 10305*l - 15650*m == -8863847)
s.add(-47499*a + 57856*b +13477*c - 10219*d -  5032*e - 21039*f - 29607*g +55241*h -  6065*i + 16047*j -  4554*k -  2262*l + 18903*m == -747805)
s.add(-65419*a + 17175*b - 9410*c - 22514*d - 52377*e -  9235*f + 53309*g +47909*h - 59111*i - 41289*j - 24422*k + 41178*l - 23447*m == -11379056)
s.add(  1805*a +  4135*b -16900*c + 33381*d + 46767*e + 58551*f - 34118*g -44920*h - 11933*i - 20530*j + 15699*k - 36597*l + 18231*m == -166140)
s.add(-42941*a + 61056*b -45169*c + 41284*d -  1722*e - 26423*f + 47052*g +42363*h + 15033*i + 18975*j + 10788*k - 33319*l + 63680*m == 9010363)
s.add(-37085*a - 51590*b -17798*c - 10127*d - 52388*e + 12746*f + 12587*g +58786*h -  8269*i + 22613*j + 30753*k - 20853*l + 32216*m == -4169825)
s.add( 36650*a + 47566*b -33282*c - 59180*d + 65196*e +  9228*f - 59599*g -62888*h + 48719*i + 47348*j - 37592*k + 57612*l + 40510*m == 4081505)
s.add( 51735*a + 35879*b -63890*c +  4102*d + 59511*e - 21386*f - 20769*g +26517*h + 28153*i + 25252*j - 43789*k + 25633*l +  7314*m == 1788229)
print s.check()
print s.model()
```

>$ python solverZ3.py  
sat   
[i = 104,    
 f = 105,  
 b = 97,  
 a = 77,  
 d = 104,  
 g = 115,  
 k = 114,  
 l = 100,  
 m = 33,  
 h = 32,  
 c = 116,  
 e = 32,  
 j = 97]  
 
>$ ./baby-re   
Var[0]: 77  
Var[1]: 97  
Var[2]: 116  
Var[3]: 104  
Var[4]: 32  
Var[5]: 105  
Var[6]: 115  
Var[7]: 32  
Var[8]: 104  
Var[9]: 97  
Var[10]: 114  
Var[11]: 100  
Var[12]: 33  
The flag is: Math is hard!  

