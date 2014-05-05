import os
import json
from otto import alteration
from otto import settings

WAV_FILE_NAME = 'say.wav'
BEEP_LOW_NAME = 'beep_lo.wav'
BEEP_HIGH_NAME = 'beep_hi.wav'


def convert_phrase_to_audio_file(self, phrase, filepath):
    os.system("espeak %s -vdefault+m3 -p 40 -s 160 --stdout > %s" % (json.dumps(phrase), filepath))


def play_audio_file(self, filepath):
    os.system("aplay -D hw:1,0 %s" % filepath)


class Voice(object):

    def __init__(self):
        self.say_file_path = os.path.join(settings.AUDIO_FOLDER, WAV_FILE_NAME)
        self.beep_high_file_path = os.path.join(settings.AUDIO_FOLDER, BEEP_HIGH_NAME)
        self.beep_low_file_path = os.path.join(settings.AUDIO_FOLDER, BEEP_LOW_NAME)

    def say(self, phrase):
        # alter phrase before speaking
        phrase = alteration.clean(phrase)
        convert_phrase_to_audio_file(phrase, self.say_file_path)
        play_audio_file(self.say_file_path)

    def play_beep_low(self):
        play_audio_file(self.beep_low_file_path)

    def play_beep_high(self):
        play_audio_file(self.beep_high_file_path)
