import wave
import audioop
import pyaudio
from tempfile import TemporaryFile
from contextlib import contextmanager
from collections import deque


THRESHOLD_MULTIPLIER = 2.8
RATE = 16000
CHUNK = 1024
FPS = RATE / CHUNK

# number of seconds to listen before forcing restart
LISTEN_TIME = 10

# number of frames to average for threshold when checking if phrase has ended
LISTEN_SILENCE_TIMEOUT = 1.5

try:
    import pocketsphinx as ps
except:
    import pocketsphinx as ps


audio = pyaudio.PyAudio()


def play_file(file_path):
    wf = wave.open(file_path, 'rb')

    stream = audio.open(
        format=audio.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    wf.close()
    stream.stop_stream()
    stream.close()


@contextmanager
def open_read_stream():
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    yield stream

    stream.stop_stream()
    stream.close()


class Mic(object):

    def __init__(self):

        self.onset_decoder = ps.Decoder(
            lm='assets/language/onset.lm',
            dict='assets/language/onset.dict',
            kws='computer'
        )

        self.decoder = ps.Decoder()

    def listen_until(self, threshold, wait_time=10, buffer_time=1):
        print 'Listening for disturbance over', threshold
        with open_read_stream() as stream:
            for _ in xrange(RATE / CHUNK * wait_time):
                current_frame = stream.read(CHUNK)
                score = self.score_audio(current_frame)
                print 'Listening', _, score
                if score > threshold:
                    return [current_frame] + [stream.read(CHUNK) for _ in xrange(RATE / CHUNK * buffer_time)]

    def get_local_threshold(self, samples=10):
        total_score = 0
        with open_read_stream() as stream:
            for _ in xrange(samples):
                total_score += self.score_audio(stream.read(CHUNK))
        return (total_score / samples) * THRESHOLD_MULTIPLIER

    def score_audio(self, data):
        """
        Returns the root-mean-square (power) of the audio signal.
        """

        rms = audioop.rms(data, 2)
        score = rms / 3
        return score

    def transcribe_with(self, frames, decoder):
        tmp_file = TemporaryFile()
        tmp_file.writelines(''.join(frames))
        tmp_file.seek(0)
        decoder.decode_raw(tmp_file)
        tmp_file.close()
        return decoder.get_hyp()

    def start_listening(self, onset_phrase):

        onset_frames = None
        phrase_frames = None

        # First, uppercase our onset phrase for consistency.
        onset_phrase = onset_phrase.upper()

        # Get local threshold
        local_threshold = self.get_local_threshold()
        play_file('assets/audio/beep_hi.wav')

        # Start a listener for audio frames above threshold
        onset_frames = self.listen_until(local_threshold)

        # If we got something above the threshold, let's check
        # to see if it contains our onset phrase.
        if onset_frames:
            onset_hyp = self.transcribe_with(onset_frames, self.onset_decoder)

            if onset_phrase in onset_hyp[0].upper():
                play_file('assets/audio/beep_hi.wav')
                phrase_frames = self.record_until(local_threshold)
                play_file('assets/audio/beep_lo.wav')

        if phrase_frames:
            return self.transcribe_with(phrase_frames, self.decoder)

    def record_until(self, threshold):
        print 'Recording until under', threshold
        with open_read_stream() as stream:

            frames = []
            scores = deque(maxlen=FPS * LISTEN_SILENCE_TIMEOUT)

            for _ in xrange(0, FPS * LISTEN_TIME):

                data = stream.read(CHUNK)
                score = self.score_audio(data)

                frames.append(data)
                scores.append(score)

                print 'Recording', _, score

                if len(scores) >= FPS * LISTEN_SILENCE_TIMEOUT:
                    average = sum(scores) / float(FPS * LISTEN_SILENCE_TIMEOUT)
                    if average < threshold:
                        break

        return frames
