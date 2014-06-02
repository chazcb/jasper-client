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

    def score(self, frames):
        """
        Returns the root-mean-square (power) of the audio signal.
        """
        return audioop.rms(frames, 2)

    def next(self):
        frames = self.stream.read(FRAMES_PER_BUFFER)
        return frames, self.score(frames)


@contextmanager
def audio_reader():
    """
    Open a new PortAudio session for input.
    """
    reader = AudioReader()
    yield reader
    reader.close()


class Mic(object):

    def get_disturbance(self):
        """
        oldest ******** | ---- newest
                  c1       c2

        `previous_score` is the rms over c1 + 3 std deviations of c2.

        If the current rms is greater than the mean of the previous scores,
        we increment our disturbance counter. Otherwise we decrement the counter.

        At any point, if the counter is greater than half the number
        of total frames we are measuring, we consider it to be a disturbance!
        """
        # Keep a 2 second audio buffer at all times.
        sample_length = 30
        frames_buffer = deque(maxlen=sample_length)

        subsequent_disturbances = 0
        recording_disturbance = False

        with audio_reader() as reader:

            ambience = np.array([reader.next()[1] for _ in xrange(sample_length)])
            mean, stdv = np.mean(ambience), np.std(ambience)
            threshold = mean + (3 * stdv)

            while True:
                frames, current_score = reader.next()
                frames_buffer.append(frames)

                if current_score > threshold:
                    subsequent_disturbances += 1
                elif subsequent_disturbances > 0:
                    # Falloff by half
                    subsequent_disturbances -= 1

                # If we have more than a half-second of audio disturbances
                # recorded in a row, then start recording.
                if subsequent_disturbances > 7:
                    subsequent_disturbances = 7
                    recording_disturbance = True

                print subsequent_disturbances, '*' if recording_disturbance else ''

                # Finally, if we're recording a disturbance and we have no
                # more frames w/ subsequent_disturbances, we return our recorded frames.
                if recording_disturbance and subsequent_disturbances == 0:
                    return ''.join(frames_buffer), current_score

                # # print curr_buffer
                # # print prev_buffer
                # print "*" * 8
                # print sum(prev_buffer) / 4.0
                # print  * tolerance

                # if (sum(curr_buffer) / 8.0) * tolerance > sum(prev_buffer) / 4.0:

                # # scores_buffer.appendleft(current_score)

                # We want to detect a disturbance if the average of the
                # last 1 second is greater than the average
                # for the previous 2 seconds (by some tolerance), and

                # if len(frames_buffer) >= 12:

                    # thresh_buffer.appendleft(current_score)

                    # p = percentile(list(scores_buffer), 95)

                    # rolling_score = sum(scores_buffer) / float(len(scores_buffer))

                    # print p, current_score * tolerance

                    # if p < current_score * tolerance:

                # tolerance = max(scores_buffer) - min(scores_buffer)
                # print "*" * 4
                # print tolerance
                # print sum(scores_buffer) / float(len(scores_buffer)) - tolerance
                # print score

                # # If current energy / previous (or rolling) energy > tolerance

        # print 'DONE yay'
                # if sum(scores_buffer) / float(len(scores_buffer)) - tolerance < score:


    # def listen_until(self, threshold, wait_time=10, buffer_time=1):

    #     scores = deque(maxlen=FPS * LISTEN_SILENCE_TIMEOUT)

    #         for _ in xrange(FPS * wait_time):
    #             frames = reader.next()
    #             score = self.score_audio(frames)
    #             print 'Listening', _, score
    #             if score > threshold:
    #                 return [frames] + [
    #                     reader.next()
    #                     for _ in xrange(FPS * buffer_time)
    #                 ]

    # def get_local_threshold(self, samples=10):
    #     total_score = 0
    #     with audio_reader() as stream:
    #         for _ in xrange(samples):
    #             total_score += self.score_audio(stream.next())
    #     return (total_score / samples) * THRESHOLD_MULTIPLIER


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
