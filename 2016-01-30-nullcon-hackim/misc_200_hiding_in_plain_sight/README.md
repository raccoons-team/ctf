# Hiding In Plain Sight.

> Find out the secret key hidden in these packets!

We got three pcap files containing only ICMP packets. Extracting data from it, we get gibberish data. After trying random
things on it, we found that rotating each byte by 42 (binary Caesar cipher), we get ASCII text - mostly non-letters, but 
at least not binary. One of decoded files contained string `---this cannot be the key---`, so we knew we were on good track.
One of those also had the string: 

```
ZWNobyAiZiIKZWNobyAibCIKZWNobyAiYSIKZWNobyAiZyIKZWNobyAieyIKZWNo
byAibWQ1c3VtIgplY2hvICIoJ2ZsãYWcnKSIKZWNobyAifSIK
```
Base64 decoded, it gave:
```
echo "f"
echo "l"
echo "a"
echo "g"
echo "{"
echo "md5sum"
echo "('flag')"
echo "}"
```
Flag is obvious now.
