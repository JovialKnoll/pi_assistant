#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request

import keyboard


TEMP_FILE_NAME = 'temp.mp3'
keys = None
with open('keys.json') as file:
    keys = json.load(file)


def speak(text):
    try:
        # grab tts file from google
        command = ('wget --quiet --timeout=5 -U Mozilla -O "{}"'
        ' "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={}"').format(
            TEMP_FILE_NAME,
            text
        )
        exit_code = subprocess.call(command, shell=True)
        # play tts file in vlc
        play_command = 'vlc --quiet -I dummy --play-and-exit {}'.format(TEMP_FILE_NAME)
        # if grabbing file failed, instead use espeak
        if exit_code != 0:
            play_command = 'espeak -v en-us+f3 -g 5 "{}"'.format(text)
        # play sound
        subprocess.call(play_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        # clear out temp file
    finally:
        if os.path.exists(TEMP_FILE_NAME):
            os.remove(TEMP_FILE_NAME)


def get_celsius(kelvin):
    return kelvin - 273.15


def get_fahrenheit(celsius):
    return (celsius * 9/5) + 32


def get_weather(location):
    url = 'https://api.openweathermap.org/data/2.5/weather?appid={}&q={}'.format(
        keys['openweathermap'],
        urllib.parse.quote(location)
    )
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    content = response.read()
    weather_dict = json.loads(content)
    if weather_dict['cod'] == '404':
        return "I wasn't able to figure out the weather."
    temp_k = float(weather_dict['main']['temp'])
    temp_c = get_celsius(temp_k)
    temp_f = get_fahrenheit(temp_c)
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


def get_location():
    url = 'https://ipinfo.io/?token={}'.format(
        keys['ipinfo']
    )
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    content = response.read()
    ipinfo_dict = json.loads(content)
    return '{}, {}'.format(
        ipinfo_dict['city'],
        ipinfo_dict['country']
    )


def get_information():
    location = get_location()
    weather = get_weather(location)
    return """
You are in or near {}.
{}""".format(
        location,
        weather
    )


def tell_information():
    info = get_information()
    print(info)
    speak(info)


def handle_key(key):
    print(key)


def main():
    keyboard.on_press(handle_key)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
sys.exit()
