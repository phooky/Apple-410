#!/usr/bin/python3
import sys
import math
import cairo
import struct

alpha_ft_start = 0x2569
point_ft_start = 0x3153

f = open("ROM.bin","rb")
data = f.read()


def eot(ft, off):
    "Returns true if the offset is at the end of the table."
    # Presumes that every table terminates in 0xff
    return data[ft + off*2] == 0xff

def get_char(ft,off):
    achar = chr(off+0x20)
    o1 = ft + (off*2)
    o2 = (data[o1+1]*256) + data[o1]
    o3 = o2
    while data[o3] != 0xff:
        o3 += 1
    return data[o2:o3]    

def unpack_byte(b):
    "convert two 4-bit signed packed numbers to a tuple"
    def sign4b(x):
        # not... quite two's complement
        if x > 8:
            return x - 16
        return x
    return (sign4b(b>>4), sign4b(b % 16))

# H:W for a char is 3:2
def unpack_coords(b,xscale=66,yscale=100,xoff=10,yoff=10):
    "convert two 4-bit signed packed numbers to cairo coordinates"
    (x,y) = unpack_byte(b)
    return (x*xscale + xoff, (8 - y)*yscale + yoff)

def build_char_file(path, ft, offset):
    surf = cairo.SVGSurface(path, 1000, 1000)
    c = cairo.Context(surf)
    d = list(get_char(ft, offset))
    c.set_source_rgb(0, 0, 0)
    c.set_line_width(20)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    while d:
        cmd = d.pop(0)
        cn, ca = cmd >> 4, cmd % 16
        for _ in range(ca):
            (x,y) = unpack_coords(d.pop(0))
            if cn == 0:
                c.move_to(x,y)
            elif cn == 2:
                c.line_to(x,y)
    c.stroke()
    surf.finish()

def dump_font(path_base, ft, charoff):
    off = 0
    while not eot(ft, off):
        build_char_file("{}_{:2x}.svg".format(path_base,charoff+off),ft,off)
        off += 1

dump_font("alpha",alpha_ft_start,0x20)

