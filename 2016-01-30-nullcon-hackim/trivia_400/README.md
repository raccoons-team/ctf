# Trivia Question 4

> Use the file. Get the flag. But, you know what, I hate pipes.

The file contained program written in Ook programming language. Running it gives string:
```
starting from 0.0.0.0, print the following IPs. 
7277067th IP Address
7234562th IP Address
7302657th IP Address
91238th IP Address
746508th IP Address
7211531th IP Address
7300098th IP Address
7211788th IP Address
723558th IP Address
91248th IP Address
7237378th IP Address
723557th IP Address
7234562th IP Address
723567th IP Address
749067th IP Address

Hint: Anything specific about all the IPs?
```
Decoding those IP addresses to octet form, we get:
```
['0.111.10.10', '0.110.100.1', '0.111.110.0', '0.1.100.101', '0.11.100.11', '0.110.10.10', 
'0.111.100.1', '0.110.11.11', '0.11.10.101', '0.1.100.111', '0.110.111.1', '0.11.10.100', 
'0.110.100.1', '0.11.10.110', '0.11.110.10']
```
We can notice they all contain only 0's and 1's, so we treated them as ASCII characters to get string 
`zi|esjyougotivz`. After deleting `|` character (see description of task), the string was the expected flag.
