#!/usr/bin/env python

import os
import subprocess
import sys

import RPi.GPIO as GPIO

TEMP_FILE_NAME = 'temp.mp3'

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
    speak("this is a test phrase")

if __name__ == '__main__':
    main()

sys.exit()
