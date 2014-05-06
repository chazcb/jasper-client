import json
import re
import os

from otto import settings

WAV_FILE_NAME = 'say.wav'
BEEP_LOW_NAME = 'beep_lo.wav'
BEEP_HIGH_NAME = 'beep_hi.wav'


YEAR_REGEX = re.compile(r'(\b)(\d\d)([0-9]\d)(\b)')


def detect_years(text):
    return YEAR_REGEX.sub('\g<1>\g<2> \g<3>\g<4>', text)


def clean_phrase(text):
    """
    Manually adjust output text before it's translated into
    actual speech by the TTS system. This is to fix minior
    idiomatic issues, for example, that 1901 is pronounced
    "one thousand, ninehundred and one" rather than
    "nineteen ninety one".

    Arguments:
    text -- original speech text to-be modified
    """
    return detect_years(text)


def convert_phrase_to_audio_file(phrase, filepath):
    os.system("espeak %s -vdefault+m3 -p 40 -s 160 --stdout > %s" % (json.dumps(phrase), filepath))


def play_audio_file(filepath):
    os.system("aplay -D %s" % filepath)


class Voice(object):

    def __init__(self):
        self.say_file_path = os.path.join(settings.AUDIO_FOLDER, WAV_FILE_NAME)
        self.beep_high_file_path = os.path.join(settings.AUDIO_FOLDER, BEEP_HIGH_NAME)
        self.beep_low_file_path = os.path.join(settings.AUDIO_FOLDER, BEEP_LOW_NAME)

    def say(self, phrase):
        # alter phrase before speaking
        phrase = clean_phrase(phrase)
        convert_phrase_to_audio_file(phrase, self.say_file_path)
        play_audio_file(self.say_file_path)

    def play_beep_low(self):
        play_audio_file(self.beep_low_file_path)

    def play_beep_high(self):
        play_audio_file(self.beep_high_file_path)
