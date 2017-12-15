#!/usr/bin/python3

import apple410
import random
import math

# 2394 x 1700
w=2394
h=1700
import sys

ring1 = 1
ring2 = 4

if len(sys.argv) > 2:
    ring1 = int(sys.argv[1])
    ring2 = int(sys.argv[2])
a = apple410.Apple410('/dev/ttyUSB0')
a.send("VP0,0,{},{}".format(w,h))
for i in range(ring1, ring2+1):
    a.send("PS{}".format(i))
    for x in range(2):
        vw = 5 + (random.random() * 100)
        vh = 5 + (random.random() * 100)
        cx = vw/2
        cy = vh/2
        r = (min(vw,vh)-1)/2
        a.send("WD0,0,{},{}".format(math.floor(vw),math.floor(vh)))
        a.send("CA{:.2f},{:.2f},{:.2f}".format(r,cx,cy))

a.send("CH")
a.send("RS")

