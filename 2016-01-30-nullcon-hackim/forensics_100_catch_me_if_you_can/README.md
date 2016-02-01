# CatchMeIfYouCan

> We got this log which is highly compressed. Find the intruder's secret.

In this task we got a file that is compressed many times using various compression algorithms. Thankfully `file` comamnd
recognizes all of them, which enables us to write a generic decompression script (`decompress.sh`). On the final layer,
there was a couple of files containing multiple Gist GitHub links - most of them were not working though. Looking through 
some of them, there was [this one](https://gist.github.com/anonymous/ac2ce167c3d2c1170efe), containg an obfuscated JS algorithm, which gave us flag when executed.
