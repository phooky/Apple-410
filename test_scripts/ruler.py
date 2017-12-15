#!/usr/bin/python3

import apple410
import random
import math

import sys

ring1 = 1
ring2 = 4

def label(point):
    (x,y) = point
    a.send("MA{},{}".format(x-100,y-40))
    a.send("PL({},{})".format(x,y))

def line(f,t):
    a.send("MA{},{}".format(f[0],f[1]))
    a.send("DA{},{}".format(t[0],t[1]))

a = apple410.Apple410('/dev/ttyUSB0')
a.send("CH")
a.send("RS")
a.send("VP0,0,1500,1500")
a.send("WD0,0,1200,1200")
a.send("LS30")

ps = [(100,100),(1100,100),(1100,1100),(100,1100)]
for p in ps:
    label(p)

for i in range(4):
    line(ps[i],ps[(i+1)%4])
a.send("CH")
a.send("RS")

