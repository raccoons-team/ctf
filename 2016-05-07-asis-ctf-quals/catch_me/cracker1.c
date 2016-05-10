#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>


char xor_with_this[0x21]="\xb1\x19\x04\xa1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00";
char flag[0x21]="\x87\x29\x34\xc5\x55\xb0\xc2\x2d\xee\x60\x34\xd4\x55\xee\x80\x7c\xee\x2f\x37\x96\x3d\xeb\x9c\x79\xee\x2c\x33\x95\x78\xed\xc1\x2b\x00";
  
const char *flag1=flag;
const char *flag2=flag+16;
const char *xor1=xor_with_this;

unsigned long entry_point=0x400440;

void func_flag_ok()
{
  printf("%s\n",flag1);
}

int check(void)
{ 
  /*
   xor=0x601060
   flag1=0x6010a0
   flag2=0x6010b0
   func_flag_ok=0x4005ed
*/
  
  
  __asm__(
        "xor %rax, %rax\n\t" //$rax=0
	"xor %rdx, %rdx\n\t" //$rax=0
	"beginning:\n\t"
        "mov %rax,%rdx\n\t" //$rdx=$rax
        "and $0x7,%edx\n\t" 
        "movzbl 0x601060(%rdx),%edx\n\t" //xor_with_this
        "xor %dl,0x6010a0(%rax)\n\t"    //flag1
        "add $0x1,%rax\n\t"
        "cmp $0x21,%rax\n\t"
        "jne beginning\n\t"
        "movdqa 0x6010a0,%xmm0\n\t" //flag1 //"movdqa 0x200c8b(%rip),%xmm0 # 0x601280\n\t"
        "pxor %xmm4,%xmm4\n\t"
        "movdqa %xmm0,%xmm1\n\t"
        "pxor %xmm2,%xmm2\n\t"
        "punpcklbw %xmm4,%xmm1\n\t"
        "punpckhbw %xmm4,%xmm0\n\t"
        "movdqa %xmm1,%xmm3\n\t"
        "punpckhwd %xmm2,%xmm1\n\t"
        "punpcklwd %xmm2,%xmm3\n\t"
        "paddd %xmm3,%xmm1\n\t"
        "movdqa %xmm0,%xmm3\n\t"
        "punpckhwd %xmm2,%xmm0\n\t"
        "punpcklwd %xmm2,%xmm3\n\t"
        "paddd %xmm3,%xmm1\n\t"
        "paddd %xmm1,%xmm0\n\t"
        "movdqa 0x6010b0,%xmm1\n\t" //flag2 //"movdqa 0x200c5b(%rip),%xmm1 # 0x601290\n\t"
        "movdqa %xmm1,%xmm3\n\t"
        "punpckhbw %xmm4,%xmm1\n\t"
        "punpcklbw %xmm4,%xmm3\n\t"
        "movdqa %xmm3,%xmm4\n\t"
        "punpckhwd %xmm2,%xmm3\n\t"
        "punpcklwd %xmm2,%xmm4\n\t"
        "paddd %xmm4,%xmm0\n\t"
        "paddd %xmm3,%xmm0\n\t"
        "movdqa %xmm1,%xmm3\n\t"
        "punpckhwd %xmm2,%xmm1\n\t"
        "punpcklwd %xmm2,%xmm3\n\t"
        "paddd %xmm3,%xmm0\n\t"
        "paddd %xmm1,%xmm0\n\t"
        "movdqa %xmm0,%xmm1\n\t"
        "psrldq $0x8,%xmm1\n\t"
        "paddd %xmm1,%xmm0\n\t"
        "movdqa %xmm0,%xmm1\n\t"
        "psrldq $0x4,%xmm1\n\t"
        "paddd %xmm1,%xmm0\n\t"
        "movd %xmm0,%eax\n\t"
        "cmp $0x954,%eax\n\t"
        "je must_jump_here\n\t"
        "jmp bad_flag\n\t"
	"must_jump_here:\n\t"
        "callq 0x4005ed\n\t" //func_flag_ok
	"bad_flag:\n\t"
	"xor %rax, %rax"
   );
}

int main(int argc, char**argv)
{
  char org_xor_with_this[0x21]="\xb1\x19\x04\xa1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00";
  char org_flag[0x21]="\x87\x29\x34\xc5\x55\xb0\xc2\x2d\xee\x60\x34\xd4\x55\xee\x80\x7c\xee\x2f\x37\x96\x3d\xeb\x9c\x79\xee\x2c\x33\x95\x78\xed\xc1\x2b\x00";

  
  printf("xor=%p\n",xor1);
  printf("flag1=%p\n",flag1);
  printf("flag2=%p\n",flag2);
  printf("func_flag_ok=%p\n",func_flag_ok);
  
  
  for(unsigned int ch1=0;ch1<=255;ch1++)
  for(unsigned int ch2=0;ch2<=255;ch2++)
  for(unsigned int ch3=0;ch3<=255;ch3++)
  for(unsigned int ch4=0;ch4<=255;ch4++)
  {
    memcpy(xor_with_this,org_xor_with_this,0x21);
    memcpy(flag,org_flag,0x21);
    
    unsigned char c1=(unsigned char)ch1;
    unsigned char c2=(unsigned char)ch2;
    unsigned char c3=(unsigned char)ch3;
    unsigned char c4=(unsigned char)ch4;
    
    unsigned char *tmp=xor_with_this;
    tmp[4]=c1;
    tmp[5]=c2;
    tmp[6]=c3;
    tmp[7]=c4;
    
    check();

  }

  return 0;
} 
