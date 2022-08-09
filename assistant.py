#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request

import keyboard


SHUTDOWN_COMMAND = 'sudo shutdown -P now'
SRC_DIRECTORY = os.path.dirname(__file__)
KEY_FILE = os.path.join(SRC_DIRECTORY, 'keys.json')
TEMP_FILE_NAME = os.path.join(SRC_DIRECTORY, 'temp.mp3')
KEY_IPINFO = 'ipinfo'
KEY_OPENWEATHERMAP = 'openweathermap'
keys = None
with open(KEY_FILE) as file:
    keys = json.load(file)


def clearTempFile():
    if os.path.exists(TEMP_FILE_NAME):
        os.remove(TEMP_FILE_NAME)


def speak(text):
    try:
        print(text)
        # grab tts file from google
        command = ('wget --quiet --timeout=5 -U Mozilla -O "{}"'
        ' "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={}"').format(
            TEMP_FILE_NAME,
            text
        )
        exit_code = subprocess.call(command, shell=True)
        # play tts file in vlc
        play_command = 'mpg123 {}'.format(TEMP_FILE_NAME)
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
    return '{}, {}'.format(
        ipinfo_dict['city'],
        ipinfo_dict['country']
    )


def getInformation():
    location = getLocation()
    weather = getWeather(location)
    return (
        "You are in or near {}.".format(location),
        weather,
    )


def tellInformation():
    info = getInformation()
    for section in info:
        speak(section)


def handleKey(key):
    if key.name == '1':
        tellInformation()
    elif key.name == '2':
        print("function 2")
    elif key.name == '3':
        print("function 3")
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
