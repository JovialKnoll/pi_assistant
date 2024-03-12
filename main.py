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


# pin setup
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
up_button = digitalio.DigitalInOut(board.D6)
up_button.switch_to_input()
up_switch = Debouncer(up_button)
down_button = digitalio.DigitalInOut(board.D5)
down_button.switch_to_input()
down_switch = Debouncer(down_button)

# display init
display = Adafruit_SSD1680(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy)

PAGE_COUNT = 2
REFRESH_SECONDS = 10 * 60

class ImageThread(threading.Thread):
    def __init__(self, images, refreshes, thread_id, get_image, delay):
        super(ImageThread, self).__init__(daemon=True)
        self.images = images
        self.refreshes = refreshes
        self.thread_id = thread_id
        self.get_image = get_image
        self.delay = delay

    def run(self):
        #image = get_image()
        #compare image to self.images[self.id], if there is a difference:
        #    self.images[self.thread_id] = image
        #    self.locks[self.thread_id].acquire()
        #    self.refreshes[self.thread_id] = True
        #    self.locks[self.thread_id].release()
        time.sleep(self.delay)


def dummy():
    pass


def main():
    images = [None] * PAGE_COUNT
    refreshes = [True] * PAGE_COUNT
    #locks = [threading.Lock()] * PAGE_COUNT
    threads = []
    threads.append(ImageThread(images, refreshes, 0, dummy, 10 * 60))
    threads.append(ImageThread(images, refreshes, 1, dummy, 1 * 60))
    for thread in threads:
        thread.start()
    page_index = 0

    while True:
        up_switch.update()
        down_switch.update()
        if up_switch.fell:
            page_index -= 1
            page_index %= PAGE_COUNT
            refreshes[page_index] = True
        if down_switch.fell:
            page_index += 1
            page_index %= PAGE_COUNT
            refreshes[page_index] = True
        if refreshes[page_index]:
            # also check if display can be refreshed
            print(f"display page: {page_index}")
            display.fill(Adafruit_EPD.WHITE)
            display.display()
            refreshes[page_index] = False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("exiting")
sys.exit()
