## Apple 410 ROM dumps

This directory contains the raw ROM dumps from the Apple 410 Color Plotter.

`B9801Y[LMN].bin` are images the three 8K 27C64 chips installed on the board. `ROM.bin` is the
consolidated ROM image built by concatenating the three individual roms.

`test_extractor.py` is a script for extracting the self-test commands from the consolidated
ROM file.

