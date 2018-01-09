## Apple 410 ROM dumps

This directory contains the raw ROM dumps from the Apple 410 Color Plotter.

`B9801Y[LMN].bin` are images the three 8K 27C64 chips installed on the board. `ROM.bin` is the
consolidated ROM image built by concatenating the three individual roms.

`test_extractor.py` is a script for extracting the self-test commands from the consolidated
ROM file.

'font_extract.py' extracts the font as a set of SVG files. 'font_to_pickled_dict.py' generates
two pickle files, one with the font and another with the point markers. Each pickle file contains
a single dictionary mapping characters to the raw sequence of bytes that represents the glyph in
the Apple 410's native format.

'ff_import.py' is a rough script for importing the SVGs into fontforge. The generated font will
require a lot of manual cleanup.

