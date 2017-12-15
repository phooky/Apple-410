#!/usr/bin/python3
import serial
import time
from plot_to_svg import Plotter

def plot_to_svg(instream, outstream):
    "Convert a set of plot instructions to an SVG. Works mininmally."
    p = Plotter()
    p.read(instream)
    p.write(outstream)

class Apple410:
    """A simple class for queing up commands for the Apple 410"""
    def __init__(self, portname, baud=9600):
        self.serial = serial.Serial(portname, baud, rtscts=True, dsrdtr=True, timeout=0.1)
        self.pos = (0,0)
        self.wd = self.vp = (0,0,2394,1759)

    def sendchar(self, c):
        self.serial.flush()
        while not self.serial.cts:
            time.sleep(0.2)
        while not self.serial.dsr:
            time.sleep(0.2)
        self.serial.write(c.encode('ascii'))
        self.serial.flush()
        
    def send(self, command):
        for c in command:
            self.sendchar(c)
        self.sendchar('\x03')

    def move_to(self, coords):
        self.send('MA{},{}'.format(coords[0],coords[1]))
        self.pos = coords

    def draw_to(self, coords):
        self.send('DA{:.2f},{:.2f}'.format(coords[0],coords[1]))
        self.pos = coords
            
    def pen_select(self, index):
        self.send('PS{}'.format(index))
    
