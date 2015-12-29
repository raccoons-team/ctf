# Writeup for HD44780 task

> Solves: 40
> 
> The logic states of the GPIOs have been recorded Figure out the displayed message. You're gonna need this here.

We are given a .tgz file containing dumps of Raspberry Pi GPIO (pin) states as a function of time, and several 
pictures showing the connections. In our solution, we did not use the pictures, as the name of the task was all we needed.
HD44780 is a protocol for communicating with character displays, needing six pins. Four of them are used as character data
(sent in two nibbles each), E pin, which was basically a clock, and RS pin, which was a switch between writing mode and
command mode.

A short inspection allowed us to guess that GPIO8 was E pin, since it was toggling very frequently, and
GPIO7 was RS pin, since it was mostly 1 (write mode), switching to 0 only a couple of times. The rest of pins we assumed were
in order, and they actually were, i.e. GPIO18=d4, GPIO23=d5, GPIO24=d6, GPIO25=d7.

We created a short Python script to parse the data to a more friendly format: (time, (filename, new_pin_state)) tuples.
Then, we looped over all data as it came in time and whenever E pin was falling (i.e. clock triggered), it meant that a
new nibble was printed.

Our initial code was just printing the characters as they came (only when RS was in write mode), giving the following text:
```
Welcome to the 32C3 The flag 32C3_Never__gonna_give_you_up_ _let_you_down_Never_EOM                 bit.ly/1fKy1tC      
```
Of course, we submitted the flag, but it turned out to be incorrect, even with or without the "EOM" or the redundant
space and underscores. Finally, we realized
that the RS pin was used sometimes too. It turned out that control characters done with RS in control mode were meaning:
"go to position (x,y) on the screen" - and that means that message could be not in order. Our final code prints:
```
Set DDRAM to:  0x0
Welcome to the 32C3 
Set DDRAM to:  0x40
The flag 32C3_Never_
Set DDRAM to:  0x54
_gonna_give_you_up_ 
Set DDRAM to:  0x14
_let_you_down_Never_
Set DDRAM to:  0x0
EOM                 
Set DDRAM to:  0x40
bit.ly/1fKy1tC      
```
Since DDRAM meant position, the text was definitely scrambled. Since the lines were starting at addresses: 
0x00, 0x40, 0x14, 0x54 (found on the Internet), the text was actually: 
```
Welcome to the 32C3 
The flag 32C3_Never_
_let_you_down_Never_
_gonna_give_you_up_ 
```
The flag glued together in this order was working just fine.
