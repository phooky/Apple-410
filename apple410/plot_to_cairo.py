#!/usr/bin/python3
import sys
import math
import cairo

def coordlist(line,expected=-1):
    l = list(map(float,line.split(',')))
    if expected > -1:
        assert len(l) == expected
    return l

pens = [
    (0, 0, 0),
    (100, 0, 0),
    (0, 100, 0),
    (0, 0, 100) ]

# Default W/H
W = 2394
H = 1759
LW = 5

class CairoPlotter:

    def __init__(self, path):
        self.surface = cairo.SVGSurface(path, W, H)
        self.context = cairo.Context(self.surface)
        #self.context.scale(W,H)
        self.context.select_font_face("monospace")
        self.pennum = 0
        self.viewport = (0, 0, W, H)
        self.window = (0, 0, W, H)
        self.text_theta = 0
        self.text_size = 1
        self.update_ctm()

    # A quick review of coordinate systems:
    # Cairo native: origin at upper left, x+ to right, y+ down.
    # Plotter native: origin at lower left, x+ to right, y+ up.
    # Plotter window: same as plotter native.
    # We want to display in plotter native.
    def update_ctm(self):
        v,w = self.viewport,self.window
        xs = (v[2]-v[0])/(w[2]-w[0])
        ys = (v[3]-v[1])/(w[3]-w[1])
        x0 = v[0] - w[0]*xs
        y0 = v[1] - w[1]*ys
        window_m = cairo.Matrix(xx=xs, yy=ys, x0=x0, y0=y0)
        pn_to_cn = cairo.Matrix(yy=-1.0, y0=H)
        self.context.set_matrix(window_m.multiply(pn_to_cn))
        self.context.set_line_width(LW)
        self.context.reset_clip()
        self.context.rectangle(w[0],w[1],w[2]-w[0],w[3]-w[1])
        self.context.clip()

    def update_font(self):
        m = cairo.Matrix(xx=self.text_size, yy=-self.text_size)
        m2 = cairo.Matrix.init_rotate(math.radians(self.text_theta))
        self.context.set_font_matrix(m.multiply(m2))

    def finish_path(self):
        cp = self.context.get_current_point()
        self.context.save()
        self.context.set_matrix(cairo.Matrix())
        self.context.stroke()
        self.context.restore()
        self.context.move_to(cp[0],cp[1])

    def vp(self, params):
        l=coordlist(params,4)
        self.viewport=(l[0],l[1],l[2],l[3])
        self.update_ctm()

    def wd(self, params):
        l=coordlist(params,4)
        self.window=(l[0],l[1],l[2],l[3])
        self.update_ctm()
    
    def ma(self, params):
        l=coordlist(params,2)
        self.context.move_to(l[0],l[1])

    def mr(self, params):
        l=coordlist(params,2)
        p=self.context.get_current_point()
        self.context.move_to(p[0]+l[0],p[1]+l[1])

    def da(self, params):
        l=coordlist(params)
        while len(l) > 0:
            x, y, l = l[0],l[1],l[2:]
            self.context.line_to(x,y)

    def dr(self, params):
        l=coordlist(params)
        while len(l) > 0:
            x, y, l = l[0],l[1],l[2:]
            p=self.context.get_current_point()
            self.context.line_to(p[0]+x,p[1]+y)

    def ca(self, params):
        self.context.new_sub_path()
        l=coordlist(params)
        r=l[0]
        if len(l) > 2:
            p=(l[1],l[2])
        else:
            p=self.context.get_current_point()
        self.context.arc(p[0],p[1],r,0.0,math.pi*2)

    def ac(self,params):
        l=coordlist(params)
        r=l[0]
        if len(l) > 3:
            p=(l[3],l[4])
        else:
            p=self.context.get_current_point()
        t1, t2 = math.radians(l[1]),math.radians(l[2])
        self.context.new_sub_path()
        self.context.arc(p[0],p[1],r,t1,t2)

    def lr(self,params):
        self.text_theta = float(params)
        self.update_font()

    def ls(self,params):
        self.text_size = float(params)
        self.update_font()

    def ps(self,params):
        self.finish_path()
        self.pennum = int(params) - 1
        p = self.pennum
        self.context.set_source_rgb(pens[p][0],pens[p][1],pens[p][2])

    def pl(self,params):
        self.finish_path()
        (x,y) = self.context.get_current_point()
        sys.stderr.write("text at {} {}\n".format(x,y))
        self.context.show_text(params)

    def write(self,out):
        self.finish_path()
        self.surface.finish()

    def process_cmd(self,command):
        cmd_code = command[0:2].lower()
        params = command[2:]
        try:
            getattr(self,cmd_code)(params)
        except AttributeError:
            sys.stderr.write("Unrecognized command code {}\n".format(cmd_code))

    def read(self,inf):
        for line in inf.readlines():
            line = line.strip()
            self.process_cmd(line)

if __name__=='__main__':
    p = CairoPlotter('foo.svg')
    p.read(sys.stdin)
    p.write(sys.stdout)

