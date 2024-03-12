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

from PIL import Image, ImageDraw, ImageFont

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
KEY_FILE = os.path.join(SRC_DIRECTORY, 'keys.json')
KEY_IPINFO = 'ipinfo'
KEY_OPENWEATHERMAP = 'openweathermap'
keys = None
with open(KEY_FILE) as file:
    keys = json.load(file)


def getCelsius(kelvin):
    return kelvin - 273.15


def getFahrenheit(celsius):
    return (celsius * 9/5) + 32


def getWeather(location):
    url = 'https://api.openweathermap.org/data/2.5/weather?appid={}&q={}'.format(
        keys[KEY_OPENWEATHERMAP],
        urllib.parse.quote(location)
    )
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    content = response.read()
    weather_dict = json.loads(content)
    if weather_dict['cod'] == '404':
        return "I wasn't able to figure out the weather."
    temp_k = float(weather_dict['main']['temp'])
    temp_c = getCelsius(temp_k)
    temp_f = getFahrenheit(temp_c)
    return """
The temperature is {} degrees Celsius, {} degrees Fahrenheit.
The humidity is {} percent.
Wind speed is {} meters per second.
The weather is described as {}.""".format(
        round(temp_c, 1),
        round(temp_f, 1),
        weather_dict['main']['humidity'],
        weather_dict['wind']['speed'],
        weather_dict['weather'][0]['description']
    )


def getLocation():
    url = 'https://ipinfo.io/?token={}'.format(
        keys[KEY_IPINFO]
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


def getInformation():
    location, time_zone = getLocation()
    weather = getWeather(location)
    return (
        "You are in or near {}.".format(location),
        weather,
    )


def get_blank_image():
    return Image.new("RGB", (constants.WIDTH, constants.HEIGHT), color=WHITE)


def get_page_0():
    image = get_blank_image()
    draw = ImageDraw.Draw(image)
    draw.text(
        (0, 0), "page 0", font=medium_font, fill=BLACK,
    )
    draw.text(
        (50, 50), "page 0", font=medium_font, fill=BLACK,
    )
    draw.text(
        (100, 100), "page 0", font=medium_font, fill=BLACK,
    )
    return image


def get_page_1():
    image = get_blank_image()
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


def get_page_2():
    image = get_blank_image()
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
