# -*- coding: utf-8 -*-

import sys
from traceback import format_exc

# The below is a bit of a mess because of Kodi vs not Kodi imports
# This allows for unit testing this module..

try:
    from .common import *
except:
    from common import *
sys.path.append(CWD + '/resources/lib/')
sys.path.append(CWD + '/resources/lib/yoctopuce')
try:
    from yocto_api import *
    from yocto_display import *
except:
    from yoctopuce.yocto_api import *
    from yoctopuce.yocto_display import *


class YoctoMaxiDisplay:
    # By default, all these are empty references
    display = None
    module = None
    drawingLayer = None
    displayLayer = None

    @staticmethod
    def register_yocto_API():
        """
        Register the Yocto API to use a USB attached device
        :return: None
        """
        log("register_yocto_API")
        errmsg = YRefParam()
        # Setup the API to use local USB devices
        if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
            log("Could not init Yocto API: " + str(errmsg))
            if unit_testing:
                sys.exit("Could not init Yocto API")

    @staticmethod
    def register_display_and_module():

        log("register_display_and_module")

        YoctoMaxiDisplay.display = YDisplay.FirstDisplay()
        if not YoctoMaxiDisplay.display and unit_testing:
            sys.exit("Couldn't find the display")

        YoctoMaxiDisplay.module = YoctoMaxiDisplay.display.get_module()
        if not YoctoMaxiDisplay.module and unit_testing:
            sys.exit("Couldn't find the module")

        log(f'Registered display {YoctoMaxiDisplay.display} and module {YoctoMaxiDisplay.module}')

    @staticmethod
    def describe_display():

        log("describe_display")

        if YoctoMaxiDisplay.display.isOnline():
            try:
                log(f'Display found: {YoctoMaxiDisplay.display.describe()} - '
                    f'Display type: {YoctoMaxiDisplay.display.get_displayType()} - '
                    f'Friendly name: {YoctoMaxiDisplay.display.get_friendlyName()}')
            except Exception as inst:
                log("Exception in describe display..." + format_exc(inst))
        else:
            log("Can't describe_display - display not online?")

    @staticmethod
    def set_brightness(brightness):

        log("set_brightness " + str(brightness))

        YoctoMaxiDisplay.display.set_brightness(brightness)

    @staticmethod
    def set_led(on):

        log(f'set_led {on}')

        if on != 'false':
            YoctoMaxiDisplay.module.set_luminosity(50)
        else:
            YoctoMaxiDisplay.module.set_luminosity(0)

    @staticmethod
    def toggle_led():

        log("toggle_led")

        led = YoctoMaxiDisplay.module.get_luminosity()
        log(f'LED was at luminosity {led}')

        if led == 50:
            YoctoMaxiDisplay.module.set_luminosity(0)
        else:
            YoctoMaxiDisplay.module.set_luminosity(50)

        led = YoctoMaxiDisplay.module.get_luminosity()
        log(f'LED now at luminosity {led}')

    @staticmethod
    def initialise_layers():
        """
        Set up simple double buffering
        :return:
        """
        log("initialise_layers")

        # Start clean
        YoctoMaxiDisplay.display.resetAll()

        # Which way is up?
        YoctoMaxiDisplay.display.set_orientation(YDisplay.ORIENTATION_RIGHT)
        # First get the layers
        YoctoMaxiDisplay.displayLayer = YoctoMaxiDisplay.display.get_displayLayer(0)
        YoctoMaxiDisplay.drawingLayer = YoctoMaxiDisplay.display.get_displayLayer(1)
        YoctoMaxiDisplay.displayLayer.clear()
        YoctoMaxiDisplay.drawingLayer.clear()

        # the drawingLayer is initially set to hidden, the display to shown....simple double buffering
        YoctoMaxiDisplay.drawingLayer.hide()
        YoctoMaxiDisplay.displayLayer.unhide()

    @staticmethod
    def display_text(lines):
        """
        To draw:
        Clear drawing layer
        Draw text
        Swap drawing layer into display layer

        Fonts built-in into the device firmware are:
        Small.yfm (height: 8 pixels)
        Medium.yfm (height: 16 pixels)
        Large.yfm (height: 32 pixels)
        8x8.yfm (monospaced)

        :return: None
        """

        log(f'display_text {lines}')

        YoctoMaxiDisplay.drawingLayer.clear()
        number_of_lines = len(lines)

        if number_of_lines == 1 or number_of_lines == 2:
            # 32 pixel high font, but there is a baseline so up to two lines should be ok.
            YoctoMaxiDisplay.drawingLayer.selectFont("Large.yfm")
        elif number_of_lines == 3 or number_of_lines == 4:
            # 16 pixel high font, but there is a baseline so up to four lines should be ok.
            YoctoMaxiDisplay.drawingLayer.selectFont("Medium.yfm")

        if number_of_lines == 1:
            YoctoMaxiDisplay.drawingLayer.drawText(64, 32, YDisplayLayer.ALIGN.CENTER, lines[0])
        elif number_of_lines == 2:
            YoctoMaxiDisplay.drawingLayer.drawText(64, 1, YDisplayLayer.ALIGN.TOP_CENTER, lines[0])
            YoctoMaxiDisplay.drawingLayer.drawText(64, 32, YDisplayLayer.ALIGN.TOP_CENTER, lines[1])
        elif number_of_lines == 3:
            YoctoMaxiDisplay.drawingLayer.drawText(64, 1, YDisplayLayer.ALIGN.TOP_CENTER, lines[0])
            YoctoMaxiDisplay.drawingLayer.drawText(64, 22, YDisplayLayer.ALIGN.TOP_CENTER, lines[1])
            YoctoMaxiDisplay.drawingLayer.drawText(64, 44, YDisplayLayer.ALIGN.TOP_CENTER, lines[2])
        elif number_of_lines == 4:
            YoctoMaxiDisplay.drawingLayer.drawText(64, 1, YDisplayLayer.ALIGN.TOP_CENTER, lines[0])
            YoctoMaxiDisplay.drawingLayer.drawText(64, 16, YDisplayLayer.ALIGN.TOP_CENTER, lines[1])
            YoctoMaxiDisplay.drawingLayer.drawText(64, 32, YDisplayLayer.ALIGN.TOP_CENTER, lines[2])
            YoctoMaxiDisplay.drawingLayer.drawText(64, 48, YDisplayLayer.ALIGN.TOP_CENTER, lines[3])
        else:
            log(f'Number of lines {number_of_lines} - not in 1 to 4 ')
            pass

        # Actually do the display...
        YoctoMaxiDisplay.display.swapLayerContent(1, 0)
        YoctoMaxiDisplay.displayLayer.unhide()

    @staticmethod
    def clean_up_display():

        log("clean_up_display")

        if YoctoMaxiDisplay.display:
            YoctoMaxiDisplay.displayLayer.clear()
            YoctoMaxiDisplay.drawingLayer.clear()
            log("Cleaned up.")
        else:
            log("Could not clean up - no display found.")


# Unit testing - simple function to cycle through 1 to 4 lines of text...
if __name__ == '__main__':

    log("__main__")

    yocto = YoctoMaxiDisplay()

    import atexit
    atexit.register(YoctoMaxiDisplay.clean_up_display)

    log("Testing Yocto MaxiDisplay")

    YoctoMaxiDisplay.register_yocto_API()
    YoctoMaxiDisplay.register_display_and_module()

    if not YoctoMaxiDisplay.display.isOnline():
        sys.exit("Error - display not online?")
    else:
        YoctoMaxiDisplay.describe_display()

    YoctoMaxiDisplay.initialise_layers()

    while True:
        log('Line 1')
        YoctoMaxiDisplay.display_text(['Line 1'])
        time.sleep(2)
        log('Line 1, Line 2')
        YoctoMaxiDisplay.display_text(['Line 1', 'Line 2'])
        time.sleep(2)
        log('Line 1, Line 2, Line 3')
        YoctoMaxiDisplay.display_text(['Line 1', 'Line 2', 'Line 3'])
        time.sleep(2)
        log('Line 1, Line 2, Line 3, Line 4')
        YoctoMaxiDisplay.display_text(['Line 1', 'Line 2', 'Line 3', 'Line 4'])
        time.sleep(2)
        # Can't really see this anyway, but it works..
        # log('Toggling LED')
        # YoctoMaxiDisplay.toggle_led()
        # time.sleep(2)
        # YoctoMaxiDisplay.toggle_led()
