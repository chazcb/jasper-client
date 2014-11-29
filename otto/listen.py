import audioop
import logging
import numpy as np

from collections import deque


log = logging.getLogger(__name__)


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
        self.threshold = 256  # a "sensible" starting threshold

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


class Listener(object):

    def __init__(self, mic):
        self.mic = mic

        # We keep 30 frames of audio (2 seconds) at all times.
        self.scorer = AudioScorer()

    def get_disturbance(self):
        """
        Returns a generator that yields fragments of disturbed
        audio (raw).
        """
        recording = False
        counter = 0

        onset = deque(maxlen=30)

        with self.mic() as mic:
            log.info('Listening for disturbance.')
            while True:
                frames = mic.next()
                onset.append(frames)

                score, has_disturbance = self.scorer.add(frames)

                if counter > 7:
                    log.info('Caught disturbance.')
                    recording = True
                elif has_disturbance:
                    counter += 1

                if recording and counter > 0:
                    counter -= 1

                # Finally, if we're recording a disturbance and we have no
                # more frames w/ counter, we return our recorded frames.
                if recording and counter < 1:
                    log.info('Disturbance ended.')
                    return iter(onset)

    def get_phrase(self):
        """
        Returns a generator that yields fragments of phrase
        audio (raw).
        """
        counter = 30  # give us a full 2 seconds of time to start

        with self.mic() as mic:
            log.info('Recording phrase.')
            while True:
                frames = mic.next()

                score, has_disturbance = self.scorer.add(frames)

                if counter < 15 and has_disturbance:
                    log.info('Recording more in phrase.')
                    counter = 15
                else:
                    counter -= 1

                if counter >= 1:
                    yield frames
