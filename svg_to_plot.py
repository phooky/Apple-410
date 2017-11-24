#!/usr/bin/python3

import sys
import re
import string
from xml.dom import minidom

coord_re = re.compile(r"([+-]?[0-9]+\.?[0-9]*),([+-]?[0-9]+\.?[0-9]*)")

def parse_coord(d):
    m = coord_re.match(d)
    coords = (float(m.group(1)),float(m.group(2)))
    remain = d[m.end():].strip()
    #print("d:{} -- {} -- {}".format(d,coords,remain))
    return (coords, remain)
    
def d_to_commands(d):
    segs = []
    (cmd, remain) = (d[0],d[1:].strip())
    if cmd == 'm':
        (coord, remain) = parse_coord(remain)
        while remain and (remain[0] == '-' or remain[0] in string.digits):
            (delta, remain) = parse_coord(remain)
            nc = (delta[0]+coord[0],delta[1]+coord[1])
            segs.append( (coord, nc) )
            coord = nc
        return segs
    return segs

            
        

# 2394 x 1700
w=2394
h=1700


if __name__ == '__main__':
    scr = '-'
    if len(sys.argv) > 1:
        scr = sys.argv[1]
    if scr == "-":
        f = sys.stdin
    else:
        f = open(scr)
    doc = minidom.parse(f)
    segs = []
    for path in doc.getElementsByTagName('path'):
        d = path.getAttribute('d')
        segs.extend(d_to_commands(d))
    #print(segs)
    maxx = max(map(lambda x: max(x[0][0], x[1][0]),segs))
    maxy = max(map(lambda x: max(x[0][1], x[1][1]),segs))
    minx = min(map(lambda x: min(x[0][0], x[1][0]),segs))
    miny = min(map(lambda x: min(x[0][1], x[1][1]),segs))
    sys.stderr.write("X {} {}\n".format(minx,maxx))
    sys.stderr.write("Y {} {}\n".format(miny,maxy))
    (spanx,spany) = (maxx-minx,maxy-miny)
    xoff = -minx
    yoff = -miny
    (s1, s2) = (1.0,1.0)
    if spanx > w:
        s1 = spanx/w
    if spany > h:
        s2 = spany/h
    s = max(s1,s2)
    xoff = xoff/s
    yoff = yoff/s
    segs = map(lambda x: ((x[0][0]/s + xoff,x[0][1]/s + yoff),
                          (x[1][0]/s + xoff,x[1][1]/s + yoff)), segs)
    for (sfrom, sto) in segs:
        print("MA{:.2f},{:.2f}\nDA{:.2f},{:.2f}".format(sfrom[0],sfrom[1],sto[0],sto[1]))
    doc.unlink()
