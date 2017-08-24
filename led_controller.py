from PIL import Image
from psd_tools import PSDImage
import numpy as np
import sys, os
import argparse


class _ledArray():
    """Base Class for a single LED data stream."""
    def __init__(self,layer,color_mode='BW'):
        self.color_mode = color_mode
        self.psd_layer = layer;
        self.name = layer.name;
        self.numLEDS = len(layer.layers);
        self.outputCount = [0 for i in xrange(self.numLEDS)];
        #self.outputFile = outputFile
        if color_mode == 'RGB':
            self.outputArray =[ [0,0,0] for i in xrange(self.numLEDS)]
        else:
            self.outputArray = [0 for i in xrange(self.numLEDS)]
    def generateOutput(self,effect):
        outputString = "const uint8_t " + self.name + "_" + effect+"[] =  {"
        outputArray = [outputString]
        for byte in self.outputArray:
            outputArray.append(str(byte));
            outputArray.append(", ");
        del outputArray[-1]
        outputArray.append("}");
        outputString = ''.join([a for a in outputArray])
        print ""
        print outputString
        print ""
    def updateAverage(self,index,value):
        if (self.color_mode == "RGB"):
            count = self.outputCount[index] = self.outputCount[index] + 1;
            oldMean = self.outputArray[index]
            for i in xrange(3):
                self.outputArray[index][i] = oldMean[i] + (value[i]-oldMean[i])/count
        else:

            count = self.outputCount[index] = self.outputCount[index] + 1;
            oldMean = self.outputArray[index]
            self.outputArray[index] = oldMean + (value-oldMean)/count            

verbose = False;

def vprint(statement):
    if (verbose):
        print statement


def parser_init():
    parser = argparse.ArgumentParser(
            description = 'Creates bitmaps using Photoshop files of LED layouts for unconventional led layouts.');
    parser.add_argument("-m", "--mask",nargs=1,required=True,  help="Photoshop file of the LED positions.")
    parser.add_argument("-i", "--input",nargs=1,required=True, help="Photo (or Folder) of the input to overlay on to the LEDS. This should be the same pixel size as the mask!")
    # parser.add_argument("-o", "--output",nargs=1,  type=argparse.FileType('w'), default=sys.stdout, help="Photoshop file of the LED positions.")
    parser.add_argument("-c", "--color_mode",nargs="?", default="RGB", help="Color mode of input image: (L,RGB)")    
    parser.add_argument("-v", "--verbose", action='store_true', help="Increase verbosity of ouput")    
    # parser.add_argument("--labelled", action='store_true', help="Only use this if you have individually labelled all the layers of the leds in your image, otherwise, it is assumed that the LED are placed in order")    

    return parser;
def main():
    #build parser options
    parser = parser_init();

    args = parser.parse_args()
    global verbose
    verbose = args.verbose;
    mask = args.mask[0]
    color_mode = args.color_mode
    vprint("Input File: " + args.input[0])

    #open image and convert to given color mode
    if (os.path.isfile(args.input[0])):
        vprint("Input File: " + args.input[0])
        files = [args.input[0]]
    elif os.path.isdir(args.input[0]):
        vprint("Using folder: " + args.input[0])
        files = os.listdir(args.input[0])
        files = [args.input[0] +"/"+ f for f in files]
    #open photoshop image
    maskPSD = PSDImage.load(mask)
    maskPIL = maskPSD.as_PIL();
    maskPIL = maskPIL.convert("1"); #this convert mask to a bitmap
    maskMeta = maskPSD.header           
    for file in files:
        if (color_mode == "1"):
            overlay = Image.open(args.input[0]).convert(1)
        else:
            overlay = Image.open(file).convert(color_mode)
        # check if the dimesions of the mask and the overlay are the same
        if ((maskMeta.width != overlay.width) and (maskMeta.height != overlay.height)):
            raise("Incorrect Size - Please apply a effect input file that is the same size as the LED Mask")

        maskLayers = [ _ledArray(layer,color_mode) for layer in maskPSD.layers ]
        vprint("Found " + str(len(maskLayers)) + " LED data lines")
        vprint("These are the following layers:")
        for layer in maskLayers:
            vprint("   " + layer.name)
        print ""
        print ""

        # this is the meat of the function
        for ledArray in maskLayers:
            numLEDS = ledArray.numLEDS;
            for i,led in enumerate(ledArray.psd_layer.layers):
                # since layers loaded most to least recent, first led is the last in the led stream
                index = numLEDS - i-1;
                x1,y1,x2,y2 = led.bbox;
                # print "(",x1,y1,x2,y2,")"
                # loop through bounding box and look for average value
                # bbox doesnt return a tranformed bbox so we need to check if
                # the pixel in the box is also part of the "led"
                for x in xrange(x1,x2):
                    for y in xrange(y1,y2):
                        pixel = maskPIL.getpixel((x,y))
                        if (pixel == 0):
                            # we have found a pixel, calculate average value
                            intensity = overlay.getpixel((x,y))
                            ledArray.updateAverage(index,intensity);
            name = os.path.splitext(file)[0];
            name = os.path.basename(name)
            ledArray.generateOutput(name)


if __name__ == '__main__':
    main()