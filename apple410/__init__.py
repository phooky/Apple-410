#!/usr/bin/python3
import serial
import time
from .plot_to_svg import Plotter

def plot_to_svg(instream, outstream):
    "Convert a set of plot instructions to an SVG. Works mininmally."
    p = Plotter()
    p.read(instream)
    p.write(outstream)

class Apple410Common:
    def __init__(self):
        self.pos = (0,0)
        self.wd = self.vp = (0,0,2394,1759)

    def move_to(self, coords):
        self.send('MA{},{}'.format(coords[0],coords[1]))
        self.pos = coords

    def draw_to(self, coords):
        self.send('DA{:.2f},{:.2f}'.format(coords[0],coords[1]))
        self.pos = coords
            
    def pen_select(self, index):
        self.send('PS{}'.format(index))

class Apple410(Apple410Common):
    """A simple class for queing up commands for the Apple 410"""
    def __init__(self, portname, baud=9600, flow_control_safe=False, cts_hack=False):
        Apple410Common.__init__(self)
        self.serial = serial.Serial(portname, baud, rtscts=False, dsrdtr=True, timeout=0.1)
        self.flow_control_safe = flow_control_safe
        self.cts_hack = cts_hack

    def sendchar(self, c):
        if self.flow_control_safe:
            self.serial.write(c.encode('ascii'))
        elif self.cts_hack:
            self.serial.flush()
            while not self.serial.cts:
                time.sleep(0.2)
            self.serial.write(c.encode('ascii'))
            self.serial.flush()
        else:
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

    def close(self):
        self.serial.close()

class MockApple410(Apple410Common):
    def __init__(self, path):
        Apple410Common.__init__(self)
        if type(path) == type(''):
            self.f = open(path,'w')
        else:
            self.f = path

    def send(self, command):
        self.f.write(command)
        self.f.write('\n')

    def close(self):
        self.f.close()

