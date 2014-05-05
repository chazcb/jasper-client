from unittest import TestCase
from exam import Exam
from exam import before, patcher

from otto.voice import Voice


class TestVoice(Exam, TestCase):

    convert_phrase = patcher('otto.voice.convert_phrase_to_audio_file')
    play_file = patcher('otto.voice.play_audio_file')

    @before
    def set_up(self):
        self.voice = Voice()

    def test_file_path(self):
        self.assertIn('say.wav', self.voice.say_file_path)

    def test_say(self):
        self.voice.say('Hello World')
        self.convert_phrase.assert_called_with('Hello World', self.voice.say_file_path)
        self.play_file.assert_called_with(self.voice.say_file_path)

    def test_beep_high(self):
        self.voice.play_beep_high()
        self.play_file.assert_called_with(self.voice.beep_high_file_path)

    def test_beep_low(self):
        self.voice.play_beep_low()
        self.play_file.assert_called_with(self.voice.beep_low_file_path)
