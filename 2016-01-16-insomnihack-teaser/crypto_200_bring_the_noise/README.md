# Bring the noise
> Quantum computers won't help you

We are given source of Python server. First thing it does is forcing us to generate string, whose
MD5 digest ends with a given 2.5 bytes - simple proof of work. Then we are given system of 40 "equations" with 6 unknowns.
The trick is that they have random vibration added, so that right hand side is always +/-1 of true result. Also, all
arithmetic is made modulo 8.

Solution:

6 unknowns with 8 possibilities each gives a grand total of 8^6, or about 250000. This is reasonable search space. We need
to rank the solution candidates somehow though - in our solution, we simply summed error (defined as difference between
left and right sides) over all equations and chose solution with smallest error. Script (`solve.py`) worked on the first try.
