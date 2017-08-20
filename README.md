# LED Display Controller


Dillinger is a command-line tool to generate output arrays for addressable leds built on non-standard layout (e.g. custom PCB layouts or just arranged strips)

# How to:

  - The commandline tool takes an input mask (as a PSD file, where each led is a seperate layer). An effect image of the same size, and an ouput file (default is stdout)
Usage:
    python LED_controller.py -m LEDMASK.psd -e FADE1.png


### Install
Requires:
* Python
* PIL 
* PSD_tools
