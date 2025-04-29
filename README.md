==Installation

Once you've checked out the Apple-410 repository, the simplest way to install it is using pip:
```
$ cd Apple-410
$ pip install --user .
```

On some systems, you may have to do this in a virtual environment or specify break-system-packages:
```
$ pip install --user --break-system-packages .
```

==Scripts

Aside from installing the apple410 package, pip with also install several convenience scripts:

* apple410 - write a plotter file directly to an Apple 410 plotter
* a410plot2png - convert a plotter file to a PNG (useful for generating previews)
* a410plot2svg - convert a plotter file to an SVG file (useful for generating previews)
* a410svg2plot - convert an SVG file to an Apple 410-ready plotter file

