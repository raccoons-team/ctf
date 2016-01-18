# Smartcat

In this task we were given a simple web application, which given an IP, pings it.
It also writes command it tried to execute, for example "ping -c 1 8.8.8.8". 
Immediately we thought there is potential for command line shell inection. However, when
we tried pinging "8.8.8.8;ls", it returned "bad character" - so there was some black list
of forbidden characters - including space.

After a while, we found that newline character is not forbidden, so we can execute for
example:
```
8.8.8.8
ls
```
After listing all files recursively using `du`, we find a flag file in an obfuscated directory.
Direct access to it is forbidden, however we can use `cat<this/some/file` to print it, which
gives flag.

In the second part we were told to exploit the same application in such a way, that it will
give us a shell. Restriction of character set stumped us for a while (remember, no spaces!), but
after a while we managed to write an exploit. It relied on `sh` builtin `<<` redirection, which
allows for any string being redirected into stdin. Thus, we could write:
```
python>/tmp/somefile<<EOF
print"test\x20test"
EOF
```
This gives us an arbitrary string in a file. Later we execute `bash</tmp/somefile` to actually
execute it as a shell command, now with spaces allowed. We uploaded a reverse shell, and got
a flag.
