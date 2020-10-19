#!/usr/bin/env python

import os
import subprocess
import sys

import RPi.GPIO as GPIO

TEMP_FILE_NAME = 'temp.mp3'
BUTTON_1 = 27
BUTTON_2 = 5
BOUNCE_TIME = 500

def speak(text):
    # grab tts file from google
    command = 'wget --quiet --timeout=5 -U Mozilla -O "{}"'\
        ' "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={}"'\
        .format(TEMP_FILE_NAME, text)
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

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((BUTTON_1, BUTTON_2), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_1, GPIO.FALLING, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(BUTTON_2, GPIO.FALLING, bouncetime=BOUNCE_TIME)
    while True:
        if GPIO.event_detected(BUTTON_1):
            speak("you pressed button one")
        if GPIO.event_detected(BUTTON_2):
            break

if __name__ == '__main__':
    main()

GPIO.cleanup()
sys.exit()
