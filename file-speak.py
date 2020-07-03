#!/usr/bin/env python

import sys
import subprocess

def speak_online(text):
    command = 'wget -q -U Mozilla -O "temp.mp3" "'
    command += 'https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q='
    command += text
    command += '"'
    #play_command = 'vlc --play-and-exit "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q="'
    subprocess.call(command, shell=True)

def speak(text):
    command = 'espeak -v en-us+f3 -g 5 "{}"'.format(text)
    subprocess.call(command, shell=True)

#speak("test text")

speak_online("it's ya boy with some test text")

sys.exit()
