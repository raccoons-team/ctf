# LOL

> Decode this - LOL

In this task we had to write a program, which was decoding various encodings, such as ROT13, hex encoding,
zlib compression etc. Unfortunately there was one encoding (called ro42), for which we could not write a true decoder,
because the encoding did not differentiate between letter case, while our response had to be of correct case - we simply
hardcoded responses. 

Server said we had to solve 25 of those challenges, but the counter was going up even after 25. Finally, when we solved
100 of them (WTF), this string was printed: `666p61677o6433633064696r675s69735s656173795s4p4s4p7q20`. If we change `n` to `a`,
`o` to `b` (i.e. rot13 encode it) and unhex it, we get the flag.
