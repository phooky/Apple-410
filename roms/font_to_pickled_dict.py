#!/usr/bin/python3
"""
Extract the fonts and create pickled dictionaries mapping characters to the raw binary
strings representing each entry. Parsing these strings is done in the client code.
"""

import struct
import pickle

alpha_ft_start = 0x2569
point_ft_start = 0x3153

f = open("ROM.bin","rb")
data = f.read()

def eot(ft, off):
    "Returns true if the offset is at the end of the table."
    # Presumes that every table terminates in 0xff
    return data[ft + off*2] == 0xff

def get_char(ft,off):
    "Returns the character data (sans terminating 0xff)"
    achar = chr(off+0x20)
    o1 = ft + (off*2)
    o2 = (data[o1+1]*256) + data[o1]
    o3 = o2
    while data[o3] != 0xff:
        o3 += 1
    return data[o2:o3]    


def build_char_dict(ft, first_char=0):
    offset = 0
    d = {}
    while not eot(ft,offset):
        cur_char = chr(offset+first_char)
        d[cur_char] = get_char(ft,offset)
        offset += 1
    return d

def pickle_font(path, ft, first_char=0):
    f = open(path,"wb")
    d = build_char_dict(ft,first_char)
    pickle.dump(d,f)

pickle_font("a410_chars.pickle",alpha_ft_start,ord(' '))
pickle_font("a410_points.pickle",point_ft_start)

