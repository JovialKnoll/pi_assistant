#!/usr/bin/env python

import json
import os
import subprocess
import sys
import urllib
import urllib2

import RPi.GPIO as GPIO

TEMP_FILE_NAME = 'temp.mp3'
BUTTON_1 = 27
BUTTON_2 = 5
BOUNCE_TIME = 1000

with open('keys.json') as file:
    keys = json.load(file)

def speak(text):
    # grab tts file from google
    command = 'wget --quiet --timeout=5 -U Mozilla -O "' \
        + TEMP_FILE_NAME \
        + '" "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=' \
        + text \
        + '"'
    exit_code = subprocess.call(command, shell=True)
    # play tts file in vlc
    play_command = 'vlc --quiet -I dummy --play-and-exit {}'.format(TEMP_FILE_NAME)
    # if grabbing file failed, instead use espeak
    if exit_code != 0:
        play_command = 'espeak -v en-us+f3 -g 5 "{}"'.format(text)
    # play sound
    subprocess.call(play_command, shell=True)
    # clear out temp file
    if os.path.exists(TEMP_FILE_NAME):
        os.remove(TEMP_FILE_NAME)

def get_celsius(kelvin):
    return kelvin - 273.15

def get_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def get_weather(location):
    url = 'https://api.openweathermap.org/data/2.5/weather?' \
        + 'appid=' \
        + keys['openweathermap'] \
        + '&q=' \
        + urllib.quote(location)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content = response.read()
    weather_dict = json.loads(content)
    if weather_dict['cod'] == '404':
        return "I wasn't able to figure out the weather."
    main_dict = weather_dict['main']
    temp_k = float(main_dict['temp'])
    temp_c = get_celsius(temp_k)
    temp_f = get_fahrenheit(temp_c)
    description = weather_dict['weather'][0]['description']
    wind_speed = weather_dict['wind']['speed']
    output = "The temperature is " \
        + str(round(temp_c, 2)) \
        + " degrees Celsius, " \
        + str(round(temp_f, 2)) \
        + " degrees Fahrenheit.\n" \
        + "The humidity is " \
        + str(main_dict['humidity']) \
        + " percent.\n" \
        + "Wind speed is " \
        + str(wind_speed) \
        + " meters per second.\n" \
        + "The weather is described as " \
        + description \
        + ".\n"
    return output

def get_location():
    url = 'https://ipinfo.io/?' \
        + 'token=' \
        + keys['ipinfo']
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content = response.read()
    ipinfo_dict = json.loads(content)
    return ipinfo_dict['city'] \
        + ", " \
        + ipinfo_dict['country']

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((BUTTON_1, BUTTON_2), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_1, GPIO.FALLING, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(BUTTON_2, GPIO.FALLING, bouncetime=BOUNCE_TIME)

    location = get_location()
    weather = get_weather()
    print(weather)
    speak(weather)
    #while True:
    #    if GPIO.event_detected(BUTTON_1):
    #        speak("you pressed button one")
    #    if GPIO.event_detected(BUTTON_2):
    #        break

if __name__ == '__main__':
    main()

GPIO.cleanup()
sys.exit()
