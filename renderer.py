#!/usr/bin/env python3

import sys
import os
import json
import urllib.parse
import urllib.request
import digitalio
import busio
import board
from datetime import datetime

from PIL import Image, ImageChops, ImageDraw, ImageFont

import constants

# drawing vars
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
icon_font = ImageFont.truetype("./meteocons.ttf", 48)
ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SRC_DIRECTORY = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(SRC_DIRECTORY, 'config.json')
KEY_IPINFO = 'key_ipinfo'
KEY_OPENWEATHERMAP = 'key_openweathermap'
CONFIG_CITY = 'config_city'
config = None
with open(CONFIG_FILE) as file:
    config = json.load(file)


def _get_weather(location):
    url = 'https://api.openweathermap.org/data/2.5/weather?appid={}&q={}'.format(
        config[KEY_OPENWEATHERMAP],
        urllib.parse.quote(location)
    )
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    if response.getcode() != 200:
        return None
    content = response.read()
    weather = json.loads(content)
    if weather['cod'] == '404':
        return None
    return weather


def getLocation():
    url = 'https://ipinfo.io/?token={}'.format(
        config[KEY_IPINFO]
    )
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    content = response.read()
    ipinfo_dict = json.loads(content)
    return (
        '{}, {}'.format(
            ipinfo_dict['city'],
            ipinfo_dict['country']
        ),
        ipinfo_dict['timezone'],
    )


def getTime():
    location, time_zone = getLocation()
    time_utc = datetime.now(timezone('UTC'))
    time_here = time_utc.astimezone(timezone(time_zone))
    time_str = time_here.strftime('%I:%M%p')
    return "It is now {}".format(time_str)


def _get_blank_image():
    return Image.new("RGB", (constants.WIDTH, constants.HEIGHT), color=WHITE)


def _get_celsius(kelvin):
    return kelvin - 273.15


def _get_fahrenheit(celsius):
    return (celsius * 9/5) + 32


def _weather():
    weather = _get_weather("Manhattan, US")
    weather_icon = ICON_MAP[weather["weather"][0]["icon"]]
    city_name = weather["name"] + ", " + weather["sys"]["country"]
    main = weather["weather"][0]["main"]
    temp_c = _get_celsius(weather["main"]["temp"])
    #temp_f = _get_fahrenheit(temp_c)
    temperature = "%d °C" % temp_c
    #temperature = "%d °F" % temp_f
    description = weather["weather"][0]["description"]
    description = description[0].upper() + description[1:]

    image = _get_blank_image()
    draw = ImageDraw.Draw(image)
    (font_width, font_height) = icon_font.getsize(weather_icon)
    xy = (
        constants.WIDTH // 2 - font_width // 2,
        constants.HEIGHT // 2 - font_height // 2 - 5,
    )
    draw.text(xy, weather_icon, font=icon_font, fill=BLACK)
    draw.text((5, 5), city_name, font=medium_font, fill=BLACK)
    (font_width, font_height) = large_font.getsize(main)
    xy = (5, constants.HEIGHT - font_height * 2)
    draw.text(xy, main, font=large_font, fill=BLACK)
    (font_width, font_height) = small_font.getsize(description)
    xy = (5, constants.HEIGHT - font_height - 5)
    draw.text(xy, description, font=small_font, fill=BLACK)
    (font_width, font_height) = large_font.getsize(temperature)
    xy = (
        constants.WIDTH - font_width - 5,
        constants.HEIGHT - font_height * 2,
    )
    draw.text(xy, temperature, font=large_font, fill=BLACK)
    return image


def _get_page_1():
    image = _get_blank_image()
    draw = ImageDraw.Draw(image)
    draw.text(
        (10, 10), "page 1", font=medium_font, fill=BLACK,
    )
    draw.text(
        (60, 60), "page 1", font=medium_font, fill=BLACK,
    )
    draw.text(
        (110, 110), "page 1", font=medium_font, fill=BLACK,
    )
    return image


def _get_page_2():
    image = _get_blank_image()
    draw = ImageDraw.Draw(image)
    draw.text(
        (20, 20), "page 2", font=medium_font, fill=BLACK,
    )
    draw.text(
        (70, 70), "page 2", font=medium_font, fill=BLACK,
    )
    draw.text(
        (120, 120), "page 2", font=medium_font, fill=BLACK,
    )
    return image


_pages = (
    (_weather, 10 * 60),
    (_get_page_1, 10 * 60),
    (_get_page_2, 10 * 60),
)


page_count = len(_pages)


def get_page(page_index, current_image):
    new_image = _pages[page_index][0]()
    delay = _pages[page_index][1]
    if not current_image or ImageChops.difference(current_image, new_image).getbbox():
        return new_image, delay
    return None, delay
