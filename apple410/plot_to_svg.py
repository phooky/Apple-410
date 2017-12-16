#!/usr/bin/python3
import sys
import svgwrite
import math

def coordlist(line,expected=-1):
    l = list(map(float,line.split(',')))
    if expected > -1:
        assert len(l) == expected
    return l

pens = [
    svgwrite.rgb(0, 0, 0, '%'),
    svgwrite.rgb(100, 0, 0, '%'),
    svgwrite.rgb(0, 100, 0, '%'),
    svgwrite.rgb(0, 0, 100, '%') ]

# Default W/H
W = 2394
H = 1759

class Plotter:
    def __init__(self):
        self.pennum = 0
        self.viewport = (0, 0, W, H)
        self.window = (0, 0, W, H)
        self.cur_g = None
        self.cur_d = None
        self.d = svgwrite.Drawing(profile='tiny',size=(W,H))
        self.text_theta = 0
        self.text_size = 1
        self.pos = (0,0)

    def get_g(self):
        "Return a valid group for this viewport/window"
        if not self.cur_g:
            self.cur_g = self.d.g()
            (v,w) = (self.viewport,self.window)
            a = (v[2]-v[0])/(w[2]-w[0])
            d = (v[3]-v[1])/(w[3]-w[1])
            e = v[0] - w[0]*a
            f = v[1] - w[1]*d
            # everything needs to flip on the Y axis.
            f = H-f
            d = -d
            sys.stderr.write("GROUP a {} d {} e {} f {}\n".format(a,d,e,f))
            self.cur_g.matrix(a,0,0,d,e,f)
        return self.cur_g

    def finish_g(self):
        if self.cur_g:
            self.d.add(self.cur_g)
        self.cur_g = None

    def finish_path(self):
        if self.cur_d:
            path=self.d.path(
                d=self.cur_d,
                stroke=pens[self.pennum])
            path.fill(opacity=0)
            self.get_g().add(path)
        self.cur_d = None

    def add_to_path(self, addition):
        if not self.cur_d:
            self.cur_d = "M{} {}".format(self.pos[0],self.pos[1])
        self.cur_d = self.cur_d + " " + addition

    def invalidate_window(self):
        self.finish_path()
        self.finish_g()

    def vp(self, params):
        self.invalidate_window()
        l=coordlist(params,4)
        self.viewport=(l[0],l[1],l[2],l[3])

    def wd(self, params):
        self.invalidate_window()
        l=coordlist(params,4)
        self.window=(l[0],l[1],l[2],l[3])
    
    def ma(self, params):
        l=coordlist(params,2)
        self.pos = (l[0],l[1])

    def mr(self, params):
        l=coordlist(params,2)
        self.pos = (self.pos[0]+l[0],self.pos[1]+l[1])

    def da(self, params):
        l=coordlist(params)
        self.add_to_path("L{}".format(" ".join(map(str,l))))
        self.pos = (l[-2],l[-1])

    def dr(self, params):
        l=coordlist(params)
        self.add_to_path("l{}".format(" ".join(map(str,l))))
        self.pos = (l[-2],l[-1])

    def ca(self, params):
        self.finish_path()
        l=coordlist(params)
        r=l[0]
        if len(l) > 2:
            p=(l[1],l[2])
        else:
            p=self.pos
        c=self.d.circle(center=p,r=r)
        c.fill(opacity=0)
        c.stroke(color=pens[self.pennum],opacity=100,width=2)
        self.get_g().add(c)

    def ac(self,params):
        l=coordlist(params)
        r=l[0]
        if len(l) > 3:
            p=(l[3],l[4])
        else:
            p=self.pos
        t2, t1 = math.radians(l[1]),math.radians(l[2])
        x1, y1 = p[0] + (r*math.cos(t1)), p[1] + (r*math.sin(t1))
        x2, y2 = p[0] + (r*math.cos(t2)), p[1] + (r*math.sin(t2))
        ds="M {} {} A {} {} 0 0 0 {} {}".format(x1,y1,r,r,x2,y2)
        self.add_to_path(ds)


    def lr(self,params):
        self.text_theta = float(params)

    def ls(self,params):
        self.text_size = float(params)

    def ps(self,params):
        self.finish_path()
        self.pennum = int(params) - 1

    def pl(self,params):
        self.finish_path()
        flip_pos = (self.pos[0], -self.pos[1])
        t = self.d.text(params,insert=flip_pos)
        t.rotate(self.text_theta,center=flip_pos)
        t['font-size'] = self.text_size
        g = self.d.g()
        g.add(t)
        g.matrix(1,0,0,-1,0,0)
        self.get_g().add(g)

    def write(self,out):
        self.invalidate_window()
        self.d.write(out)

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
    p = Plotter()
    p.read(sys.stdin)
    p.write(sys.stdout)

