from unittest import TestCase
from exam import Exam
from exam import before

from otto.contrib.mic.pyaudio import mic


class TestOnsetMic(Exam, TestCase):

    @before
    def set_up(self):
        self.mic = mic

    def test_is_context_manager(self):
        with self.mic() as mic:
            print mic
