# OddLED
![](https://github.com/tylerGoulding/LED_display_controller/tree/master/media/output.png)

OddLed is a command-line tool to generate output arrays for addressable leds for non-standard LED layout (e.g. custom PCB layouts or just arranged strips)

## Why
Sometimes, LEDS are a grid or straight line.. sometimes youre printing PCBS for LED text or sometimes your just aligning leds in a weird orientation. OddLED makes creating LED mappings easy

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
- First, you need to make the LED mask, each LED data line (driven by a different IO pin) should be a seperate layer and the LEDs should be paced in order of the actual LEDS. In the example below, I am adding a gradient across two diagonal rows of LEDS:
This is the LED layout:
![](https://github.com/tylerGoulding/LED_display_controller/tree/master/media/output.png)
All of the LEDs are on the same Data line thus they are all in a single group called "test". Inside the group are the leds, as simple rectangle objects. The rectangles are ordered in order of the data in the actual LEDs.  
![](https://github.com/tylerGoulding/LED_display_controller/tree/master/media/sample_layers.png)
sample_layers
  - The commandline tool takes an input mask (as a PSD file, where each led is a seperate layer). An effect image of the same size, and an ouput file (default is stdout)
Usage:
    python LED_controller.py -m LEDMASK.psd -e FADE1.png
