#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime

import keyboard
from pytz import timezone


SHUTDOWN_COMMAND = 'sudo shutdown -P now'
SRC_DIRECTORY = os.path.dirname(__file__)
KEY_FILE = os.path.join(SRC_DIRECTORY, 'keys.json')
TEMP_FILE = os.path.join(SRC_DIRECTORY, 'temp.mp3')
KEY_IPINFO = 'ipinfo'
KEY_OPENWEATHERMAP = 'openweathermap'
keys = None
with open(KEY_FILE) as file:
    keys = json.load(file)


def clearTempFile():
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)


def speak(text):
    try:
        # grab tts file from google
        command = ('wget --quiet --timeout=5 -U Mozilla -O "{}"'
        ' "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={}"').format(
            TEMP_FILE,
            text
        )
        exit_code = subprocess.call(command, shell=True)
        # play tts file in vlc
        play_command = 'mpg123 {}'.format(TEMP_FILE)
        # if grabbing file failed, instead use espeak
        if exit_code != 0:
            play_command = 'espeak -v en-us+f3 -g 5 "{}"'.format(text)
        # play sound
        subprocess.call(play_command, shell=True)
        # clear out temp file
    finally:
        clearTempFile()


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


def handleKey(key):
    if key.name == '1':
        time = getTime()
        speak(time)
    elif key.name == '2':
        info = getInformation()
        for section in info:
            speak(section)
    elif key.name == '3':
        pass
    elif key.name == '4':
        subprocess.call(SHUTDOWN_COMMAND, shell=True)


def main():
    keyboard.on_press(handleKey)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        clearTempFile()


if __name__ == '__main__':
    main()
sys.exit()
