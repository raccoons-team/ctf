# Internetwache CTF 2016: 404 Flag not found (misc 80)  


> I tried to download the flag, but somehow received only 404 errors :(

We also get network capture, with some DNS traffic and few `GET` requests. During solving this task, I was sure its something about networking and DNS querring. Man, how much I have tried DNS tricks, querring in hope to get some adress after redirect or another puzzle. 

We started to look at hostnames, those were formatted like: `67732e0a5768657468657220796f752077696e206f72206c6f736520646f.2015.ctf.internetwache.org` and in desperation nex try was to decode this hex string. It resulted with: `gs. Whether you win or lose do.` Bingo. Some filtering later we had little shattered text:

```
In the end, it's all about fla
gs.
Whether you win or lose do
esn't matter.
{Ofc, winning is
 cooler
Did you find other fla
gs?
Noboby finds other flags!

Superman is my hero.
_HERO!!!_

Help me my friend, I'm lost i
n my own mind.
Always, always,
 for ever alone.
Crying until 
I'm dying.
Kings never die.
So
 do I.
}!
```

There was idea, lets try only big letters. And flag is ours:) **IW{ODNS_HERO!!!_HIACIKSI}**

Nope. [ZONK!](https://en.wikipedia.org/wiki/Let%27s_Make_a_Deal)

But after some guessing we hav found correct flag:
**IW{DNS_HACKS}**

_Note: Looking at other writeups it could be filtered in little different way, and then you were chosing first letters from lines._

