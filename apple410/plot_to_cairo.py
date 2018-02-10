#!/usr/bin/python3
import sys
import math
import cairo
import pkg_resources
import pickle

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

class Font:
    def __init__(self,path):
        f = open(pkg_resources.resource_filename('apple410',path),'rb')
        self.char_map = pickle.load(f)


    def unpack_byte(b):
        "convert two 4-bit signed packed numbers to a tuple"
        # this packing is... unusual.
        x = b >> 4
        y = b % 16
        if y > 8: # now the weird
            x -= 1
            y -= 16
        return (x,y)

    def render_char(self, ctx, char, xoff, yoff):
        d = list(self.char_map[char])
        while d:
            cmd = d.pop(0)
            cn, ca = cmd >> 4, cmd % 16
            for _ in range(ca):
                (x1, y1) = Font.unpack_byte(d.pop(0))
                x = x1 + xoff
                y = y1 + yoff
                if cn == 0:
                    ctx.move_to(x,y)
                elif cn == 2:
                    ctx.line_to(x,y)

    def render_string(self,ctx,s):
        xoff = 0
        yoff = 0
        ctx.set_line_width(1)
        for c in s:
            if c == '\r' or c == '\n':
                xoff = 0
                yoff += 10
            elif c == '\t':
                xoff += 20
            else:
                self.render_char(ctx,c,xoff,yoff)
                xoff += 10

class CairoPlotter:

    def __init__(self, path, surftype = 'SVG'):
        self.surftype = surftype
        if surftype == 'SVG':
            self.surface = cairo.SVGSurface(path, W, H)
        elif surftype == 'PNG':
            self.path = path
            self.surface = cairo.ImageSurface(cairo.Format.RGB24,W,H)
        self.context = cairo.Context(self.surface)
        if surftype == 'PNG':
            self.context.rectangle(0,0,W,H)
            self.context.set_source_rgb(1.0,1.0,1.0)
            self.context.fill()
        #self.context.scale(W,H)
        self.context.select_font_face("monospace")
        self.pennum = 0
        self.viewport = (0, 0, W, H)
        self.window = (0, 0, W, H)
        self.text_theta = 0
        self.text_size = 1
        self.context.set_line_cap(cairo.LINE_CAP_ROUND)
        self.context.set_line_join(cairo.LINE_JOIN_ROUND)
        self.update_ctm()
        self.char_font = Font('data/a410_chars.pickle')


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
        self.finish_path()
        l=coordlist(params,4)
        self.viewport=(l[0],l[1],l[2],l[3])
        self.update_ctm()

    def wd(self, params):
        self.finish_path()
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

    def yt(self, params):
        l=coordlist(params,5)
        left = l[3]
        right = l[4]
        num = int(l[2])
        style = int(l[0])
        if style > 3:
            sys.stderr.write("Unrecognized tick mark style {}\n".format(style))
            return
        if style:
            dist = l[1]
            tw = dist/num
        else:
            dist = l[1]*num
            tw = l[1]
        first = style >> 1
        (x,y) = self.context.get_current_point()
        self.context.line_to(x,y+dist)
        for i in range(first,num+1):
            y1 = y + tw*i
            self.context.move_to(x+left,y1)
            self.context.line_to(x-right,y1)

    def xt(self, params):
        l=coordlist(params,5)
        above = l[3]
        below = l[4]
        num = int(l[2])
        style = int(l[0])
        if style > 3:
            sys.stderr.write("Unrecognized tick mark style {}\n".format(style))
            return
        if style & 0x01:
            dist = l[1]
            tw = dist/num
        else:
            dist = l[1]*num
            tw = l[1]
        first = style >> 1
        (x,y) = self.context.get_current_point()
        self.context.line_to(x+dist,y)
        for i in range(first,num+1):
            x1 = x + tw*i
            self.context.move_to(x1,y+above)
            self.context.line_to(x1,y-below)

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
        self.context.save()
        self.context.translate(x,y)
        self.context.rotate(math.radians(self.text_theta))
        self.context.scale(self.text_size/10.0, self.text_size/8.0)
        self.char_font.render_string(self.context,params)
        self.context.restore()

    def write(self):
        self.finish_path()
        if self.surftype == 'PNG':
            if self.path == '-':
                self.surface.write_to_png(sys.stdout)
            else:
                self.surface.write_to_png(self.path)
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
    p = CairoPlotter(sys.stdout.buffer)
    p.read(sys.stdin)
    p.write()

