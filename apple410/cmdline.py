import sys
import argparse

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
        f = open(scr)
    if len(sys.argv) > 1:
        scr = sys.argv[1]
    if args.svg:
        print("SVG conversion is not yet implemented!")
        sys.exit(1)
    a = Apple410(args.device,baud=args.baud)
    for line in f.readlines():
        print("Sending {}".format(line.strip()))
        a.send(line.strip())
    

