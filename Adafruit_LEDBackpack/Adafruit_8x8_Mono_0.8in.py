#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 8x8 Monochrome 0.8 inches Pixel Display
# ===========================================================================

class EightByEight:
    disp = None

    # Constructor
    def __init__(self, address=0x70, debug=False):
        if (debug):
            print "Initializing a new instance of LEDBackpack at 0x%02X" % address
        self.disp = LEDBackpack(address=address, debug=debug)

# ===========================================================================
#  A single row operations
# ===========================================================================

    def writeRowRaw(self, charNumber, value):
        "Sets a row of pixels using a raw 16-bit value"
        if (charNumber > 7):
            return
            # Set the appropriate row
        self.disp.setBufferRow(charNumber, self.wrapValue(value))

    def writeMatrix(self, mx, color=1):
        "Sets a 8x8 matrix"
        row=0;
        for value in mx:
            if (row > 7):
                return
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

    # ===========================================================================
    #  A single pixel operations
    # ===========================================================================

    def setPixel(self, x, y):
        "Sets a single pixel"
        if (x > 7) | (y > 7):
            return
        # Set the appropriate pixel
        value = 2**x
        buffer = self.disp.getBuffer()
        self.disp.setBufferRow(y, buffer[y] | self.wrapValue(value))

    def clearPixel(self, x, y):
        "Sets a single pixel"
        if (x > 7) | (y > 7):
            return
            # Set the appropriate pixel
        value = ~(2**x) & 0xFF
        buffer = self.disp.getBuffer()
        self.disp.setBufferRow(y, buffer[y] & self.wrapValue(value))

    def switchPixel(self, x, y):
        "Sets a single pixel"
        if (x > 7) | (y > 7):
            return
            # Set the appropriate pixel
        value = 2**x
        buffer = self.disp.getBuffer()
        self.disp.setBufferRow(y, buffer[y] ^ self.wrapValue(value))

    # ===========================================================================
    #
    # ===========================================================================

    def clear(self):
        "Clears the entire display"
        self.disp.clear()
