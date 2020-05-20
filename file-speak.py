#!/usr/bin/env python

import sys
import subprocess

#say() {
#    local IFS=+;
#    vlc --play-and-exit "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en";
#}
#say $*

def speak(text):
    command = 'espeak -v en-us+f3 -g 5 "{}"'.format(text)
    subprocess.call(command, shell=True)

speak("test text")

sys.exit()
