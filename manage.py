#!/usr/bin/env python
import sys
import os
import logging


import requests

# Include folder with ./manage.py as module.
sys.path.insert(1, os.path.join(os.path.dirname(__file__)))

from otto.contrib.mic.pyaudio import mic
from otto.contrib.transcribe.sphinx import PocketSphinxSTT
from otto.contrib.transcribe.wit import WitSTT
from otto.listen import Listener

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':

    listener = Listener(mic=mic)

    ps = PocketSphinxSTT()
    wit = WitSTT()

    while True:
        onset_frames = listener.get_disturbance()
        onset = ps.transcribe(onset_frames)

        print "Onset", onset

        if 'computer' in onset.lower():
            phrase_frames = listener.get_phrase()
            phrase = wit.transcribe(phrase_frames)

            logging.info('Heard "%s"', phrase)
            if 'on' in phrase:
                requests.get('https://agent.electricimp.com/QhaVzh5W-sFT?light_state=1')

            elif 'off' in phrase:
                requests.get('https://agent.electricimp.com/QhaVzh5W-sFT?light_state=0')

            if 'exit' in phrase:
                exit()
