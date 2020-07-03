#!/usr/bin/env python

import sys
import subprocess

TEMP_FILE_NAME = 'temp.mp3'

def speak(text):
    command = 'wget -q --timeout=5 -U Mozilla -O "{}"'\
        ' "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={}"'\
        .format(TEMP_FILE_NAME, text)
    exit_code = subprocess.call(command, shell=True)
    play_command = 'vlc --play-and-exit {}'.format(TEMP_FILE_NAME)
    if exit_code != 0:
        play_command = 'espeak -v en-us+f3 -g 5 "{}"'.format(text)
    subprocess.call(play_command, shell=True)

speak("good morning sir")

sys.exit()
