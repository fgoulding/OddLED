# OddLED


OddLed is a command-line tool to generate output arrays for addressable leds for non-standard LED layout (e.g. custom PCB layouts or just arranged strips)

## Features
- Written in Python
- Creates bitmaps using Photoshop files of LED layouts for unconventional led structures.
- Supports multiple LED data lines (as seperate layers in the photoshop file)
- Works with either single files as well as folders to generate full effects at a single time

## Installation
OddLED requires Python2 and a few 3rd Party Libraries
To install python on Mac:
```
brew install python
```
To install Python on Debian/Ubuntu:
```
sudo apt-get install python
```

PIP should be installed on Python 2 >=2.7.9 but if you dont have it go [here](https://pip.pypa.io/en/stable/installing/)

Once you have Pip, run:
```
pip install Pillow
```
```
pip install PSD_tools
```

# How to:

  - The commandline tool takes an input mask (as a PSD file, where each led is a seperate layer). An effect image of the same size, and an ouput file (default is stdout)
Usage:
    python LED_controller.py -m LEDMASK.psd -e FADE1.png


### Install
Requires:
* Python
* PIL 
* PSD_tools
