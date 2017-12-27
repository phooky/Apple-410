#!/usr/bin/python

import fontforge
import tempfile
import os
import re


font = fontforge.font()
font.fontname = "Apple410"
base = "alpha"
matcher = re.compile(r"{}_([0-9a-f][0-9a-f]).svg".format(base))

for path in os.listdir('.'):
    m = matcher.match(path)
    if m:
        idx = int(m.group(1),16)
        print "{} : {}".format(idx,path)
        # fontforge can't handle % colors, so we need to hack those out. Luckily, these are the only %
        # characters in the files, so...
        tf = tempfile.NamedTemporaryFile(suffix='.svg')
        inf = open(path)
        for c in inf.read():
            if c != '%':
                tf.write(c)
        tf.flush()
        font.createChar(idx)
        font[idx].importOutlines(tf.name)
        tf.close()
        inf.close()

print "glyph count {}".format(len(font))
#print font.createChar(0x41)
#font[0x41].importOutlines("alpha_41.svg")

font.save("Apple410.ttf")

