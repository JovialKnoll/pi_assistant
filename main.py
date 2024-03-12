#!/usr/bin/env python3

import sys
import time
import busio
import board
import digitalio
import threading

from adafruit_debouncer import Debouncer
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from PIL import ImageChops

import constants
import renderer


# display
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
display = Adafruit_SSD1680(constants.HEIGHT, constants.WIDTH, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy)
display.rotation = 1

# input
up_button = digitalio.DigitalInOut(board.D6)
up_button.switch_to_input()
up_switch = Debouncer(up_button)
down_button = digitalio.DigitalInOut(board.D5)
down_button.switch_to_input()
down_switch = Debouncer(down_button)

# pages
pages = (
    (renderer.get_page_0, 10 * 60),
    (renderer.get_page_1, 1 * 60),
    (renderer.get_page_2, 5 * 60),
)


class ImageThread(threading.Thread):
    def __init__(self, images, refreshes, thread_id, get_image, delay):
        super(ImageThread, self).__init__(daemon=True)
        self.images = images
        self.refreshes = refreshes
        self.thread_id = thread_id
        self.get_image = get_image
        self.delay = delay

    def run(self):
        image = self.get_image()
        print(f"got image: {self.thread_id}")
        if not self.images[self.thread_id] or ImageChops.difference(self.images[self.thread_id], image).getbbox():
            self.images[self.thread_id] = image
            self.refreshes[self.thread_id] = True
            print(f"set image: {self.thread_id}")
        time.sleep(self.delay)


def main():
    images = [None] * len(pages)
    refreshes = [True] * len(pages)
    threads = [
        ImageThread(images, refreshes, i, page[0], page[1])
        for i, page in enumerate(pages)
    ]
    for thread in threads:
        thread.start()
    page_index = 0

    while True:
        up_switch.update()
        down_switch.update()
        if up_switch.fell:
            page_index -= 1
            page_index %= len(pages)
            refreshes[page_index] = True
        if down_switch.fell:
            page_index += 1
            page_index %= len(pages)
            refreshes[page_index] = True
        if refreshes[page_index] and images[page_index]:
            print(f"displaying page: {page_index}")
            display.image(images[page_index])
            display.display()
            refreshes[page_index] = False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("exiting")
sys.exit()
