# toasted

> Welcome to Internet of Toaster! This next-gen piece of art is awaiting you!

> Pwn it on toasted.insomnihack.ch:7200 and read the /flag !

> FYI Runs chrooted so forget about your execve shellcodes.

> Coming soon to a kickstarter near you (patent pending)

We did not finish this task on time, but we were pretty close to solving it.

In this problem we were given an ARM executable running on their server. When first ran, we were greeted with a 
password prompt. Quick peek at executable showed it was just a `strcmp` with constant `How Large Is A Stack Of Toast?`.
Then we could actually deal with the meat of the binary. Here's a sample of communication:
```
Welcome to Internet of Toaster!
Featuring "Random Heat Distribution" (patent pending)
Passphrase : How Large Is A Stack Of Toast?
Access granted!
This next-gen toaster allows for 256 slices of bread !
It also has a small tank of replacement bread if you burn one, which is a huge improvement over the netbsd-based models!
Which slice do you want to heat?
1
Toasting 1!
Which slice do you want to heat?
2
Toasting 2!
Which slice do you want to heat?
255
Toasting 255!
Which slice do you want to heat?
256
Which slice do you want to heat?
999
Which slice do you want to heat?
11111111111111111111111
Which slice do you want to heat?
Which slice do you want to heat?
Which slice do you want to heat?
Which slice do you want to heat?
Which slice do you want to heat?
Toasting 111!
Which slice do you want to heat?
0
Toasting 0!
Which slice do you want to heat?
0
Toasting 0!
Detected bread overheat, replacing
Which slice do you want to heat?
0
Toasting 0!
Which slice do you want to heat?
0
Toasting 0!
Which slice do you want to heat?
0
Toasting 0!
Detected bread overheat, replacing
Which slice do you want to heat?
0
Toasting 0!
Which slice do you want to heat?
0
Toasting 0!
Detected bread overheat, replacing
Which slice do you want to heat?
0
Toasting 0!
Which slice do you want to heat?
0
Toasting 0!
Which slice do you want to heat?
0
Toasting 0!
Which slice do you want to heat?
0
Toasting 0!
Detected bread overheat, replacing
The bread reserve tank is empty... Quitting
Well, you've had your toasting frenzy!
Cheers
```
Using `strace`, we determined that the binary was always reading up to 4 characters as number, so no overflow of
input buffer was possible. We had no real idea for the next part, so we rewrote the binary into C:
```
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

// These two variables are named from symbols.
int gcanary;  // global
int overheat; // global

// Other variables are named by myself.
void show_bread(unsigned char* r0){
	unsigned char* given_buffer=r0; // offset 0x4
	int i=0;  // offset 0xc
	while(i<=0xff){
		printf("[%3hhu]", given_buffer[i]);
		if(i%16==15)
			putchar('\n');
		i++;
	}
}

void handle_bread(unsigned char* r0, int r1){
	int  show_bread_status=r1; // offset: 0
	unsigned char* given_buffer=r0; // offset: 4
	int  chosen_slice;  // offset: 0x0c
	char user_input[4]; // offset: 0x10
	int  new_bread; // offset: 0x14
	int  stack_canary=gcanary; // offset: 0x18
	int  i; // offset: 0x1c
	for(i=0;i<=0x103;i++){
		if(overheat==4){
			puts("Bread reserve empty");
			return;
		}
		if(show_bread_status!=0){
			puts("Bread status: ");
			show_bread(given_buffer); // r0=given_buffer
		}
		puts("Which slice do you want to heat?");
		read(0, user_input, 4); // 0=stdin
		if(*user_input=='q' || *user_input=='x'){
			return;
		}
		if(!sscanf(user_input, "%d", &chosen_slice)){
			continue;
		}
		if(chosen_slice>0xff){
			continue;
		}
		printf("Toasting %d\n", chosen_slice);
		new_bread=given_buffer[chosen_slice]+(rand()&0xff);
		if(new_bread>0x100){
			puts("Detected bread overheat");
			given_buffer[chosen_slice]=0;
			overheat++;
		}
		else{
			given_buffer[chosen_slice]=new_bread&0xff;
		}
		i++;
	}
	if(stack_canary!=gcanary) {
		exit(-1);
	}
	return;
}

void checkpass(char* r0){
	char* buff=r0; // offset: 0x4
	int stack_canary=gcanary; // offset: 0x8
	int read_characters=0; // offset: 0xc

	printf("Passphrase: \n");
	read_characters=read(0, buff, 0x20); // 0=stdin
	if(read_characters<0){
		exit(-1);
	}
	buff[read_characters]=0;
	if(strcmp("How Large Is A Stack Of Toast?\n", buff)){
		puts("Access denied");
		exit(-1);
	}
	if(stack_canary!=gcanary){
		exit(0);
	}
	puts("Access granted");
	return;
}

int main(int argc, char** argv){
	char** _argv=argv; // offset: 0x0
	int _argc=argc; // offset: 0x4
	union{ // offset: 0x8
		int seed_int;
		char buff[4];
	} seed;
	int debug_mode=0; // offset: 0xc
	char buff_256[0x100]; // offset: 0x10
	char buff_32[0x20]; //offset: 0x110
	int fd; // offset: 0x130
	int stack_canary; // offset: 0x134

	//setvbuf(_IO_stdout, ......); // whatever, normal stuff
	memset(buff_256, 0, 0x100);
	if(_argc>1){
		debug_mode=1;
	}
	fd=open("/dev/urandom", 0);
	read(fd, &gcanary, 4);
	stack_canary=gcanary;
	puts("Welcome & stuff");
	checkpass(buff_32);
	printf("I can toast %d toasts.\n", 0x100);
	puts("It also...");
	read(fd, seed.buff, 4);
	srandom(seed.seed_int);
	handle_bread(buff_256, debug_mode);
	puts("Well, you've had your toasting frenzy!\nCheers");
	if(gcanary!=stack_canary){
		exit(-1);
	}
	return 0;
}
```
Finally, we noticed two vulnerabilities:

1) In checkpass, we could supply exactly 0x20 characters; then there will be a single null byte overflowing. Luckily,
that one byte overwrote `fd`, or `/dev/urandom` file descriptor, allowing us to supply seed of RNG ourselves, and predict
values generated by `rand`.

2) `%d` format string allows for any number - including negative. This passes all checks and allows to overwrite
return address, hinting at ROP exploit.

Unfortunately, it is not trivial to find a seed that will generate needed exploit bytes - for instance, expected number
of `0xff` bytes in 256 random bytes is about 1, so it is unlikely that there will be enough of them. However, we could
create bytes as a sum of them (for instance, heat with a random value of 0x20, then 0x40 to get 0x60). There was one
more important constraint - we could increase values of about 256 bytes, but decrease it (actually clear it) only four
times - or three in practice. We worked around this restriction by first jumping to a large `pop` instruction, shifting
our stack pointer by a couple of tens of bytes, right into a place containing only `0x00` bytes initially. This finally
allowed us to put about 50 or 60 arbitrary bytes of explot on the stack. Some bytes where easier than others, so when
our script said it couldn't find a good seed, we had to fiddle with jump locations a bit.

We tried the following gadgets:
- "/flag\x00" string somewhere
- `pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}` to move stack pointer 36 bytes down to place with null bytes.
- `pop {r0, r1, r6, r7, pc}` to load `r0`, `r1` and `r7` (arguments to `open` syscall)
- `svc 0` and `pop {r7, pc}` - equivalent to `int 0x80; ret`
- `pop {r0, r1, r2, r3, r4, r7, pc}` - loading `r0`, `r1`, `r2` and `r7` (arguments to `write` syscall)
- `svc 0` and `pop {r7, pc}` - equivalent to `int 0x80; ret`
- `pop {r0, r2, r6, pc}` - loading `r0` (argument to `puts`)
- (puts function)

This exploit worked locally (source in `exploit.py`, although we broke some of the gadgets while fighting later...),
but for some reason server returned SIGSEGV message (standard qemu debug message). This is where we ran out of time -
most likely it had stack address in another place, thus forcing us to leak this information somehow (or if it was
constant, just semi-bruteforce it using de Bruijn pattern).
