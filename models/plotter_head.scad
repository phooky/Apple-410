notch_width = 2.5;
$fa = 8;
$fs = 0.5;
module peg_hole() {
    union() {
        difference() {
            union() {
                cylinder(h=21.5,d1=7.8,d2=7.2,center=false);
                // Chamfer
                cylinder(h=1,d1=8.2,d2=7.8,center=false);
            }
            translate([2.5, -5, -0.1]) {
                cube([10,10,30]);
            }
        }
        translate([0,-notch_width/2,0]) {
            cube([4.5,notch_width,3.4]);
        }
    }
}

module shell() {
    union() {
        cylinder(h=12,d=32.0,center=false);
        translate([0,0,8.1]) {
            cylinder(h=3.4,d=34,center=false);
        }
        translate([0,0,11.5]) {
            cylinder(h=11.4,d1=34,d2=21,center=false);
        }
    }
}

module pen(which) {
    rotate([0,0,which*90]) {
        translate([10,0,4]) rotate([0,90,0]) {
            cylinder(h=10,d=4,center=false);
        }
    }
}

module pens() {
    for (i=[0:4]) {
        pen(i);
    }
}
    
difference() {
    union() {
        shell();
    }
    pens();
    translate([0,0,-0.005]) {
        peg_hole();
    }
}