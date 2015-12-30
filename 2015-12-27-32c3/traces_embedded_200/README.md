# Writeup for traces task

> Solves: 17
> 
> Could you please decode this for me? KTHXBYE!

In this task we were given a .tar.gz containing over 500MB-long file "data.csv". Here is how it looked like:

First 30 lines:
```
Model,MDO3014
Firmware Version,1.20

Waveform Type,ANALOG,,Waveform Type,DIGITAL,,,,,,,,,,,
Point Format,Y,,Point Format,Y,,,,,,,,,,,
Horizontal Units,s,,Horizontal Units,s,,,,,,,,,,,
Horizontal Scale,0.004,,Horizontal Scale,0.004,,,,,,,,,,,
Horizontal Delay,0.019528,,,,,,,,,,,,,,
Sample Interval,4e-09,,Sample Interval,4e-09,,,,,,,,,,,
Record Length,1e+07,,Record Length,1e+07,,,,,,,,,,,
Gating,0.0% to 100.0%,,Gating,0.0% to 100.0%,,,,,,,,,,,
Probe Attenuation,10,,,,,,,,,,,,,,
Vertical Units,V,,Vertical Units,V,V,V,V,V,V,V,V,V,V,V,V
Vertical Offset,0,,Threshold Used,1.65,1.65,1.65,1.65,1.65,1.65,1.65,1.65,1.65,1.65,1.65,1.65
Vertical Scale,2,,,,,,,,,,,,,,
Vertical Position,-1.98,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,
Label,PCLK,,Label,FV,LV,D9,D8,D7,D6,D5,D4,D3,D2,D1,D0
TIME,CH1,,TIME,D11,D10,D9,D8,D7,D6,D5,D4,D3,D2,D1,D0
-4.720000e-04,0.68,,-4.720000e-04,0,0,0,0,0,0,0,0,0,0,0,0
-4.719960e-04,0.28,,-4.719960e-04,0,0,0,0,0,0,0,0,0,0,0,0
-4.719920e-04,0.2,,-4.719920e-04,0,0,0,0,0,0,0,0,0,0,0,0
-4.719880e-04,0.2,,-4.719880e-04,0,0,0,0,0,0,0,0,0,0,0,0
-4.719840e-04,1.32,,-4.719840e-04,0,0,0,0,0,0,0,0,0,0,0,0
-4.719800e-04,2.68,,-4.719800e-04,0,0,0,0,0,0,0,0,0,0,0,0
-4.719760e-04,2.92,,-4.719760e-04,0,0,0,0,0,0,0,0,0,0,0,0
-4.719720e-04,3,,-4.719720e-04,0,0,0,0,0,0,0,0,0,0,0,0
-4.719680e-04,2.92,,-4.719680e-04,0,0,0,0,0,0,0,0,0,0,0,0
```
Last 10 lines:
```
3.952796e-02,1.96,,3.952796e-02,1,1,0,0,1,0,0,1,1,1,0,0
3.952797e-02,3,,3.952797e-02,1,1,0,0,1,0,0,1,1,1,0,0
3.952797e-02,3,,3.952797e-02,1,1,0,0,1,0,0,1,1,1,0,0
3.952798e-02,3,,3.952798e-02,1,1,0,0,1,0,0,1,1,1,0,0
3.952798e-02,2.36,,3.952798e-02,1,1,0,0,1,0,0,1,1,0,1,0
3.952798e-02,0.76,,3.952798e-02,1,1,0,0,1,0,0,1,1,0,1,0
3.952799e-02,0.28,,3.952799e-02,1,1,0,0,1,0,0,1,1,0,1,0
3.952799e-02,0.28,,3.952799e-02,1,1,0,0,1,0,0,1,1,0,1,0
3.952800e-02,0.28,,3.952800e-02,1,1,0,0,1,0,0,1,1,0,1,0
```

Google says MDO3014 is a model of oscilloscope, so it is natural to assume that this is some kind of signal dump.
Columns were helpfully labelled for us: there was TIME, CH1, TIME again and D0-D11. When I plotted the only analog
signal, CH1, against time, it looked like this (with D0 overlaid):
![Clock](http://i.imgur.com/fAkL9h0.png)

As we can see, digital signal was changing only on falling edge of CH1. Thus, it is safe to assume that CH1 is clock
and we should sample digital channels on the *rising* edge of CH1. Thus, the first step of proccessing is:
```
f=open("data.csv")
fout=open("data2.csv","w")
last=1.5
for line in f.readlines()[25:-2]:
    spl=line.split(",")
    ch1=float(spl[1])
    if last<1.5 and ch1>=1.5:
        fout.write(",".join(spl[4:]))
    last=ch1
```
This gave us a file `data2.csv` looking like this (with more lines of course):
```
1,1,0,1,1,0,1,1,1,1,1,1
1,1,0,1,1,0,0,0,0,1,0,1
1,1,0,1,0,1,0,1,0,1,0,1
1,1,0,1,0,1,0,1,0,0,1,1
1,1,0,1,0,1,0,1,0,1,1,0
1,1,0,1,1,0,1,1,0,0,0,1
1,1,1,0,0,0,0,0,0,1,1,1
1,1,1,0,0,1,0,0,1,1,1,0
1,1,1,0,0,1,0,0,0,0,1,0
1,1,0,1,1,0,1,0,1,1,0,1
1,1,0,1,0,0,1,0,1,0,0,1
1,1,0,0,1,1,0,0,1,0,0,0
```
Each of the lines was just one piece of digital data at a given clock.

The next step was to perform a manual inspection of the file. It soon became obvious that the first two columns were almost
always "1", except for short bursts - and at those times, the remaining columns were all "0". We guessed that the two first
signals were used for control, and thus we discarded them and lines in which any of them was 0.

Another observation was that the remaining columns seemed to change smoothly, if interpreted as binary number, i.e. D9 was
rarely changing, while D0, the least significant bit, was almost random. Thus, we decided to change rows into their 
numerical representation. Code:
```
f=open("data2.csv")
fout=open("data3.csv","w")

for line in f.readlines():
    spl=line.strip().split(",")
    if int(spl[0])==0 or int(spl[1])==0:
        continue
    num=0
    for i in spl[2:]:
        num=num*2+int(i)
    fout.write(str(num)+"\n")
```
This gave us a list of numbers stored in "data3.csv". When plotted several thousand of those numbers against their
position, we can notice something interesting:

![Period](http://i.imgur.com/p0FDJeI.png)

The plot looks pretty periodic. Closer look tells us that the exact period of repetition is 752. Thus, we decided to make
a series of plots, each graphing only a range of data, 752 pieces long. First three graphs are available 
[here](http://imgur.com/a/gB0AN). When watched as animation (or through holding right arrow in Image Viewer),
we can see a smooth transition between "frames". However, this does not give us much useful information.

In the end, we came up with idea of plotting this as a 3D surface plot (X axis - "frame" number, Y axis - index within
"frame", Z - value). However, since at this amount of data the plot would be unreadable, we decided to instead make a
heat map in grayscale:
```
from scipy.misc import toimage

f=open("data3.csv")
data=f.readlines()
data=[int(x)//4 for x in data] # Reducing range from 1023 to 255
data2d=[]
for i in range(len(data)//752):
    data2d.append([])
    for j in range(752):
        data2d[-1].append(data[i*752+j])
toimage(data2d).save("image.png")
```
This created an image, with each pixel's brightness representing number at that point and saved it in "image.png". This
is the produced image:

![Flag](http://i.imgur.com/As0mA99.png)

As you can see, the picture makes sense (it is an oscilloscope), and a flag is visible on the screen.

As an afterthought, it is likely that the first two channels (the ones we skipped), could actually help us in going for
the flag - those were probably VSYNC and HSYNC signals. Still, we managed to do the task without their help.

