from __future__ import absolute_import

import pyaudio

from contextlib import contextmanager


class PyAudioReader(object):

    RATE = 16000
    FRAMES_PER_BUFFER = 1024

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER,
        )

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def next(self):
        return self.stream.read(self.FRAMES_PER_BUFFER)


@contextmanager
def mic():
    """
    Open a new PortAudio microphone session.
    """
    mic = PyAudioReader()
    yield mic
    mic.close()
