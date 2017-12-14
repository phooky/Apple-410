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
for i in range(ring1, ring2+1):
    a.send("PS{}".format(i))
    xc = random.random() * w
    yc = random.random() * h
    pos="{:.2f},{:.2f}".format(xc,yc)
    r=10+(random.random()*12)
    maxr=0.0
    for (tx,ty) in [(0,0),(w,0),(0,h),(w,h)]:
        (dx,dy) = (tx-xc,ty-yc)
        cr = math.sqrt(dx*dx + dy*dy)
        if cr > maxr:
            maxr = cr
    iters = math.floor(cr/r)
    for i in range(1,iters):
        a.send("CA{:.1f},{}".format(i*r,pos))

a.send("CH")
a.send("RS")

