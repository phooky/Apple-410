#!/usr/bin/python3
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import math

font_table_start = 0x2569
first_char = 0x2627

f = open("ROM.bin","rb")
data = f.read()

from gi.repository import Gtk
import cairo
import math

char_off = 0

# ! :  01 08 21 02 01 00 21 00
# " :  01 28 21 26 01 68 21 66
def get_char(ft,off):
    achar = chr(off+0x20)
    o1 = ft + (off*2)
    o2 = (data[o1+1]*256) + data[o1]
    o3 = o2
    while data[o3] != 0xff:
        o3 += 1
    #print("Looking up '{}' at {:x}; len {}".format(achar,o2,o3-o2))
    print("{} :  {}".format(achar, " ".join(map(hex,data[o2:o3]))))
    return data[o2:o3]    

def bytecoords(b):
    rx, ry = math.floor(b/16), b%16 
    if ry > 8:
        ry = ry - 16
    ry = 8 - ry  # inverted y axis
    return ( 50 + rx*16, 50 + ry*16 )

def OnDraw(w, cr):
    global char_off
    cr.set_source_rgb(0, 0, 0)
    np = True
    cr.set_line_width(5)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    data = list(get_char(font_table_start, char_off))
    pos = (0,0)
    while data:
        c = data.pop(0)
        if c == 0x01:
            # move
            (x,y) = bytecoords( data.pop(0) )
            cr.move_to(x,y)
        elif c > 0x20:
            segments = c - 0x20
            for s in range(segments):
                # draw to
                (x,y) = bytecoords( data.pop(0) )
                cr.line_to(x,y)
    cr.stroke()

def OnKey(w, event):
    global char_off
    n = Gdk.keyval_name(event.keyval)
    if n == 'Right':
        char_off += 1
        #get_char(font_table_start, char_off)
        #coords.append((x,y))
        w.queue_draw()
    elif n == 'Left':
        char_off -= 1
        #get_char(font_table_start, char_off)
        w.queue_draw()
    elif n == 'q':
        print("QUIT")
        Gtk.main_quit()

w = Gtk.Window()
w.set_default_size(640, 480)
a = Gtk.DrawingArea()
w.add(a)

w.connect('destroy', Gtk.main_quit)
a.connect('draw', OnDraw)
w.connect('key_press_event', OnKey)

w.show_all()

Gtk.main()



