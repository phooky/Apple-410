import sys
import argparse
from . import Apple410
from .svg_to_plot import plot_svg

def main():
    parser = argparse.ArgumentParser("apple410",
            description="Send a file to an Apple 410 Color Plotter.",
            epilog="""
            If you're having trouble sending commands to your plotter, double check
            that your baud rate is in agreement with the DIP switches on the back
            of your plotter and that your serial port implements hardware flow
            control.
            """)
    parser.add_argument('-d', '--device', default='/dev/ttyUSB0', 
            help='The serial port that communicates with the plotter')
    parser.add_argument('-b', '--baud', default=9600, type=int,
            help='The baud rate of the serial port')
    parser.add_argument('--svg', action='store_true',
            help='Parse input as an SVG file')
    parser.add_argument('FILE', 
            help='The file to send to the plotter. "-" will send commands from standard input.')
    args = parser.parse_args()
    if args.FILE == "-":
        f = sys.stdin
    else:
        f = open(args.FILE)
    if args.svg:
        print("SVG conversion is not yet implemented!")
        sys.exit(1)
    a = Apple410(args.device,baud=args.baud)
    for line in f.readlines():
        print("Sending {}".format(line.strip()))
        a.send(line.strip())
    
def svg2plot():
    parser = argparse.ArgumentParser("svg2plot",
            description="Convert an SVG to Apple 410 Color Plotter commands",
            epilog="This is a work in progress and only handles simple paths.")
    parser.add_argument('-c', '--center', action='store_true',
            help = 'Center the SVG')
    parser.add_argument('SVG', help='The SVG to process. "-" will read the SVG from standard input.')
    args = parser.parse_args()
    if args.SVG == '-':
        f = sys.stdin
    else:
        f = open(args.SVG)
    plot_svg(f,center=args.center)

from .plot_to_cairo import CairoPlotter

def plot2svg():
    parser = argparse.ArgumentParser("plot2svg",
            description="Convert a set of Apple 410 Color Plotter commands to an SVG")
    parser.add_argument('PLOT', help='The plotter file to process. "-" will read plotter commands from standard input.')
    args = parser.parse_args()
    if args.PLOT == '-':
        f = sys.stdin
    else:
        f = open(args.PLOT)
    p = CairoPlotter(sys.stdout.buffer)
    p.read(f)
    p.write()
    
