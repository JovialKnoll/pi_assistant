#!/usr/bin/env python

import os
import subprocess
import sys

TEMP_FILE_NAME = 'temp.mp3'

def speak(text):
    command = 'wget --quiet --timeout=5 -U Mozilla -O "{}"'\
        ' "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={}"'\
        .format(TEMP_FILE_NAME, text)
    exit_code = subprocess.call(command, shell=True)
    play_command = 'vlc --quiet -I dummy --play-and-exit {}'.format(TEMP_FILE_NAME)
    if exit_code != 0:
        play_command = 'espeak -v en-us+f3 -g 5 "{}"'.format(text)
    subprocess.call(play_command, shell=True)
    if os.path.exists(TEMP_FILE_NAME):
        os.remove(TEMP_FILE_NAME)

speak("good morning sir")

sys.exit()
