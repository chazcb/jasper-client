#!/usr/bin/env python
import sys
import os
import logging

# Include folder with ./manage.py as module.
sys.path.insert(1, os.path.join(os.path.dirname(__file__)))

from otto.contrib.mic.pyaudio import mic
from otto.contrib.transcribe.psphinx import Brain
from otto.listen import Listener

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':

    listener = Listener(mic=mic)
    b = Brain()

    while True:
        onset_frames = listener.get_disturbance()
        onset = b.transcribe(onset_frames)

        if 'computer' in onset[0].lower():
            phrase_frames = listener.get_phrase()
            phrase = b.transcribe(phrase_frames)

            logging.info('Heard "%s"', phrase[0])

            if 'exit' in phrase[0]:
                exit()
