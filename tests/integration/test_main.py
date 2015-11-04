from unittest import TestCase
import wave

from exam import Exam

from otto.contrib.transcribe.sphinx import PocketSphinxSTT
from otto.contrib.transcribe.wit import WitSTT

from otto.listen import (
    Listener,
)


class FakeMic(object):

    def __init__(self, file_path):
        self.wave = wave.open(file_path, 'r')

        print self.wave.getframerate()

        assert self.wave.getframerate() == 16000
        assert self.wave.getsampwidth() == 2L
        assert self.wave.getnchannels() == 1

        self.counter = 0

    def next(self):
        self.counter += 1
        if self.counter > 1000:
            raise StopIteration
        return self.wave.readframes(1024)

    def close(self):
        self.wave.close()


class TestListenForOnset(Exam, TestCase):

    def create_listener(self, file_path):
        return Listener(Mic=lambda: FakeMic(file_path))

    def test_sphinx_transcribe_disturbance(self):
        l = self.create_listener('tests/hal_error.wav')
        t = PocketSphinxSTT()
        result = t.transcribe(l.get_disturbance())

        print result

    def test_wit_transcribe_disturbance(self):
        l = self.create_listener('tests/hal_error.wav')
        t = WitSTT()
        result = t.transcribe(l.get_disturbance())

        print result

