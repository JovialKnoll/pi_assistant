#!/usr/bin/env python

import sys
import subprocess

TEMP_FILE_NAME = 'temp.mp3'

def speak_online(text):
    command = 'wget -q --timeout=5 -U Mozilla -O "{}"'\
        ' "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={}"'\
        .format(TEMP_FILE_NAME, text)
    exit_code = subprocess.call(command, shell=True)
    print(exit_code)
    #play_command = 'vlc --play-and-exit "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q="'

def speak(text):
    command = 'espeak -v en-us+f3 -g 5 "{}"'.format(text)
    subprocess.call(command, shell=True)

#speak("test text")

speak_online("good morning sir")

sys.exit()
