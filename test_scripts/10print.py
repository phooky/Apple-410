#!/usr/bin/python3

import apple410
import random
import math

lineht=100
# 2394 x 1700
w=2394
h=1700

a = apple410.Apple410('/dev/ttyUSB0')
a.send("LS{}".format(lineht))
ydim = math.floor(h/lineht)
xdim = math.floor(w/lineht)
for y in range(ydim):
    a.send("MA0,{}".format(lineht*y))
    a.send("PL"+''.join(map(lambda _:random.choice('\\/'),range(xdim))))
a.send("CH")
