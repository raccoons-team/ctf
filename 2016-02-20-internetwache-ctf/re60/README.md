# Internetwache CTF 2016 : File Checker

**Category:** Reversing
**Points:** 60
**Solves:** 190
**Description:**

> Description: My friend sent me this file. He told that if I manage to reverse it, I'll have access to all his devices. My misfortune that I don't know anything about reversing :/
> 
> 
> Attachment: [rev60.zip](./rev60.zip)


## Write-up
For first, we checked what file is it

> filechecker: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=564c7e61a18251b57f8c2c3dc205ed3a5b35cca6, stripped

So we have 64-bit linux binary, that after launch prints
```
./filechecker 
Fatal error: File does not exist
````
So app want file, we checked filename

```
  400666:       55                      push   rbp
  400667:       48 89 e5                mov    rbp,rsp
  40066a:       48 83 ec 30             sub    rsp,0x30
  40066e:       89 7d dc                mov    DWORD PTR [rbp-0x24],edi
  400671:       48 89 75 d0             mov    QWORD PTR [rbp-0x30],rsi
  400675:       b8 00 00 00 00          mov    eax,0x0
  40067a:       e8 e1 00 00 00          call   400760 <fopen@plt+0x200>
  40067f:       85 c0                   test   eax,eax
  400681:       75 19                   jne    40069c <fopen@plt+0x13c>
  400683:       bf d8 08 40 00          mov    edi,0x4008d8
  400688:       b8 00 00 00 00          mov    eax,0x0
  40068d:       e8 7e fe ff ff          call   400510 <printf@plt>
  400692:       b8 01 00 00 00          mov    eax,0x1
  400697:       e9 c2 00 00 00          jmp    40075e <fopen@plt+0x1fe>
  40069c:       be f9 08 40 00          mov    esi,0x4008f9
  4006a1:       bf fb 08 40 00          mov    edi,0x4008fb // password string addr
  4006a6:       e8 b5 fe ff ff          call   400560 <fopen@plt>
  ```
  At `0x4008fb` was placed `.password` string, so we have filename.
  
  Without analyzing whole file, we have seen that if variable from `[rbp-0x4]` will be equal or lower than 0, `Congrats` will be printed to stdout.

  ```
  40072c:       83 7d fc 00             cmp    DWORD PTR [rbp-0x4],0x0
  400730:       7e 11                   jle    400743 <fopen@plt+0x1e3>
  400732:       bf 20 09 40 00          mov    edi,0x400920 // Error Wrong Characters string
  400737:       e8 b4 fd ff ff          call   4004f0 <puts@plt>
```
```
 400743:       48 8b 45 f0             mov    rax,QWORD PTR [rbp-0x10]
 400747:       48 89 c7                mov    rdi,rax
 40074a:       e8 b1 fd ff ff          call   400500 <fclose@plt>
 40074f:       bf 38 09 40 00          mov    edi,0x400938 // Congrats string
 400754:       e8 97 fd ff ff          call   4004f0 <puts@plt>
  ```
  
  Value at `[rbp-x04]` depends on function at `0x40079c` so we reversed this function...
 ```
 40079c:       55                      push   rbp
 40079d:       48 89 e5                mov    rbp,rsp
 4007a0:       89 7d bc                mov    DWORD PTR [rbp-0x44],edi
 4007a3:       48 89 75 b0             mov    QWORD PTR [rbp-0x50],rsi
 4007a7:       c7 45 c0 ee 12 00 00    mov    DWORD PTR [rbp-0x40],0x12ee
 4007ae:       c7 45 c4 e0 12 00 00    mov    DWORD PTR [rbp-0x3c],0x12e0
 4007b5:       c7 45 c8 bc 12 00 00    mov    DWORD PTR [rbp-0x38],0x12bc
 4007bc:       c7 45 cc f1 12 00 00    mov    DWORD PTR [rbp-0x34],0x12f1
 4007c3:       c7 45 d0 ee 12 00 00    mov    DWORD PTR [rbp-0x30],0x12ee
 4007ca:       c7 45 d4 eb 12 00 00    mov    DWORD PTR [rbp-0x2c],0x12eb
 4007d1:       c7 45 d8 f2 12 00 00    mov    DWORD PTR [rbp-0x28],0x12f2
 4007d8:       c7 45 dc d8 12 00 00    mov    DWORD PTR [rbp-0x24],0x12d8
 4007df:       c7 45 e0 f4 12 00 00    mov    DWORD PTR [rbp-0x20],0x12f4
 4007e6:       c7 45 e4 ef 12 00 00    mov    DWORD PTR [rbp-0x1c],0x12ef
 4007ed:       c7 45 e8 d2 12 00 00    mov    DWORD PTR [rbp-0x18],0x12d2
 4007f4:       c7 45 ec f4 12 00 00    mov    DWORD PTR [rbp-0x14],0x12f4
 4007fb:       c7 45 f0 ec 12 00 00    mov    DWORD PTR [rbp-0x10],0x12ec
 400802:       c7 45 f4 d6 12 00 00    mov    DWORD PTR [rbp-0xc],0x12d6
 400809:       c7 45 f8 ba 12 00 00    mov    DWORD PTR [rbp-0x8],0x12ba
 400810:       8b 45 bc                mov    eax,DWORD PTR [rbp-0x44]
 400813:       48 98                   cdqe   
 400815:       8b 54 85 c0             mov    edx,DWORD PTR [rbp+rax*4-0x40]
 400819:       48 8b 45 b0             mov    rax,QWORD PTR [rbp-0x50]
 40081d:       8b 00                   mov    eax,DWORD PTR [rax]
 40081f:       8d 0c 02                lea    ecx,[rdx+rax*1]
 400822:       ba 33 c9 4a 35          mov    edx,0x354ac933
 400827:       89 c8                   mov    eax,ecx
 400829:       f7 ea                   imul   edx
 40082b:       c1 fa 0a                sar    edx,0xa
 40082e:       89 c8                   mov    eax,ecx
 400830:       c1 f8 1f                sar    eax,0x1f
 400833:       29 c2                   sub    edx,eax
 400835:       89 d0                   mov    eax,edx
 400837:       69 c0 37 13 00 00       imul   eax,eax,0x1337
 40083d:       29 c1                   sub    ecx,eax
 40083f:       89 c8                   mov    eax,ecx
 400841:       48 8b 55 b0             mov    rdx,QWORD PTR [rbp-0x50]
 400845:       89 02                   mov    DWORD PTR [rdx],eax
 400847:       90                      nop
 400848:       5d                      pop    rbp
 400849:       c3                      ret    
 ```
 ...and write a keygen
 ```
#include <stdio.h>
#include <stdint.h>

int16_t tab[] = {
    0x12ee, 0x12e0,
    0x12bc, 0x12f1,
    0x12ee, 0x12eb,
    0x12f2, 0x12d8,
    0x12f4, 0x12ef,
    0x12d2, 0x12f4,
    0x12ec, 0x12d6,
    0x12ba, 
};

int get_dig_for_char(int i, char cc) {
    
    int64_t sum = cc + tab[i];
    return sum-(sum*0x354ac933>>32>>0xa-(sum>>0x1f))*0x1337;
}

int main() {
    
    char flag[30] = {0};
   
    int f=0;
    for(int i=0;i<30;++i) 
        for(int a = ' '; a<'~';++a) 
            if(get_dig_for_char(i, a) == 0) 
                flag[f++] = a;
    
    printf("Flag:%s\n", flag);
}
./*
 ./keygen
 $ Flag:IW{FILE_CHeCKa}
 */
```
Thats all, folks.

 
  
  
  


  
  


