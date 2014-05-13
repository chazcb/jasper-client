from unittest import TestCase
from exam import Exam
from exam import before, patcher

from otto.voice import (
    clean_phrase,
    convert_phrase_to_audio_file,
    play_audio_file,
    Voice,
)


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


class TestConvertPhraseToAudioFile(Exam, TestCase):

    system = patcher('otto.voice.os.system')

    def test_normal_phrase(self):
        convert_phrase_to_audio_file('Hello World', 'monkey.wav')
        self.system.assert_called_with('espeak "Hello World" -vdefault+m3 -p 40 -s 160 --stdout > monkey.wav')


class TestCleanPhrase(TestCase):

    def test_normal_phrase(self):
        self.assertEqual('Hello World', clean_phrase('Hello World'))

    def test_phrase_with_date(self):
        self.assertEqual('The date is 19 01 and the time is 5.', clean_phrase('The date is 1901 and the time is 5.'))


class TestPlayAudioFile(Exam, TestCase):

    system = patcher('otto.voice.os.system')

    def test_play(self):
        play_audio_file('monkey.wav')
        self.system.assert_called_with('aplay -D sysdefault:CARD=ALSA monkey.wav')
