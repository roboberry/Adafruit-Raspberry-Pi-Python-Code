#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 8x8 Monochrome 0.8 inches Pixel Display
# ===========================================================================

class EightByEight:
    disp = None
    color = 0 # 0 = single color matrix with a huge amount bugs on the hardware

    # Constructor
    def __init__(self, address=0x70, color=0, debug=False):
        if (debug):
            print "Initializing a new instance of LEDBackpack at 0x%02X" % address
        self.disp = LEDBackpack(address=address, debug=debug)
        self.color = color

    def writeRowRaw(self, charNumber, value):
        "Sets a row of pixels using a raw 16-bit value"
        if (charNumber > 7):
            return
            # Set the appropriate row
        if (self.color):
            self.disp.setBufferRow(charNumber, value)
        else:
            self.disp.setBufferRow(charNumber, self.wrapValue(value))

    def writeMatrix(self, mx, color=1):
        "Sets a 8x8 matrix"
        row=0;
        for value in mx:
            if (row > 7):
                return
            if (self.color):
                self.disp.setBufferRow(row, value, False);
            else:
                self.disp.setBufferRow(row, self.wrapValue(value), False);
            row+=1;
        self.disp.writeDisplay();

    def wrapValue (self, value):
        "A function to mock 8x8 LED bug (offset and flip)"
        valueHI = value & 0xFF00
        valueLO = value & 0x00FF
        valueLO = ((valueLO << 1) & 0xFF)|(valueLO >> 7)
        flip = 0x00
        for i in range(8):
            flip = (flip | ((2**(7-i)) if (valueLO & 2**i) else 0))
        valueLO = flip & 0x00FF
        return valueHI | valueLO

    def clearPixel(self, x, y):
        "A wrapper function to clear pixels (purely cosmetic)"
        self.setPixel(x, y, 0)

    def setPixel(self, x, y):
        "Sets a single pixel"
        if (x > 7) | (y > 7):
            return
            # Set the appropriate pixel
        buffer = self.disp.getBuffer()
        if (self.color):
            self.disp.setBufferRow(y, buffer[y] | value)
        else:
            self.disp.setBufferRow(y, buffer[y] | wrapValue(value))

    def clear(self):
        "Clears the entire display"
        self.disp.clear()
