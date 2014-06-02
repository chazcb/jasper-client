import audioop
import pyaudio

import numpy as np

from collections import deque
from contextlib import contextmanager

from otto.settings import (
    # FPS,
    # LISTEN_SILENCE_TIMEOUT,
    # LISTEN_TIME,
    # THRESHOLD_MULTIPLIER,
    FRAMES_PER_BUFFER,
    RATE,
)


class AudioReader(object):

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
        )

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def next(self):
        return self.stream.read(FRAMES_PER_BUFFER)


@contextmanager
def audio_reader():
    """
    Open a new PortAudio session for input.
    """
    reader = AudioReader()
    yield reader
    reader.close()


class AudioScorer(object):
    """
    Calculates a score and rolling threshold for
    audio frames where:
        - `score` is the root mean square of the audio frames, and
        - `threshold` = mean(scores) + (3 * stdv(scores))

    """

    def __init__(self, frames=[], length=15):
        self.length = length
        self.scores = deque(map(self.calc_score, frames), maxlen=length)
        self.threshold = 256

    def calc_score(self, frames):
        return audioop.rms(frames, 2)

    def add(self, frames):
        """
        Calculates the score of the passed audio frames
        and checks if the score is above the current threshold.

        Returns `(score, True)` if the frames are above the current threshold.
        Otherwise we recalculate the threshold and return `(score, False)`.
        """
        score = self.calc_score(frames)
        self.scores.append(score)

        if len(self.scores) >= self.length and score > self.threshold:
            return score, True

        # This calc is slow and probably should be done
        # without deque -> numpy arrays if possible.
        mean, stdv = np.mean(self.scores), np.std(self.scores)
        self.threshold = mean + (3 * stdv)

        return score, False


class OnsetMic(object):

    def __init__(self):

        # We keep 30 frames of audio (2 seconds) at all times.
        self.frames = deque(maxlen=30)
        self.scorer = AudioScorer()

    def get_disturbance(self):

        recording = False
        counter = 0

        with audio_reader() as reader:
            while True:
                frames = reader.next()
                self.frames.append(frames)

                score, has_disturbance = self.scorer.add(frames)
                counter += 1 if has_disturbance else -1 if counter > 0 else 0

                # If we have more than 7 frames of audio disturbances  in
                # a row (a half second), then we should start recording.
                if counter > 7:
                    recording = True
                    # counter = 7

                print score, has_disturbance, counter

                # print 'r' if recording else '-', '+' if has_disturbance else '-', counter

                # Finally, if we're recording a disturbance and we have no
                # more frames w/ counter, we return our recorded frames.
                if recording and counter == 0:
                    return ''.join(self.frames)

    # def record_until(self, threshold):
    #     print 'Recording until under', threshold
    #     with audio_reader() as stream:

    #         frames = []
    #         scores = deque(maxlen=FPS * LISTEN_SILENCE_TIMEOUT)

    #         for _ in xrange(0, FPS * LISTEN_TIME):

    #             data = stream.next()
    #             score = self.score_audio(data)

    #             frames.append(data)
    #             scores.append(score)

    #             print 'Recording', _, score

    #             if len(scores) >= FPS * LISTEN_SILENCE_TIMEOUT:
    #                 average = sum(scores) / float(FPS * LISTEN_SILENCE_TIMEOUT)
    #                 if average < threshold:
    #                     break

    #     return frames
