#!/usr/bin/env python3

import sys
import busio
import board
import digitalio

from adafruit_debouncer import Debouncer
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1680 import Adafruit_SSD1680


# pin setup
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
up_button = digitalio.DigitalInOut(board.D5)
up_button.switch_to_input()
up_switch = Debouncer(up_button)
down_button = digitalio.DigitalInOut(board.D6)
down_button.switch_to_input()
down_switch = Debouncer(down_button)

# display init
display = Adafruit_SSD1680(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy)


def main():
    display.fill(Adafruit_EPD.WHITE)
    display.display()
    
    try:
        while True:
            up_switch.update()
            down_switch.update()
            if up_switch.fell:
                print("fell")
            if up_switch.rose:
                print("rose")
    except KeyboardInterrupt:
        print("exiting")


if __name__ == '__main__':
    main()
sys.exit()
