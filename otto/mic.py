
import os
import wave
import audioop
import pyaudio


THRESHOLD_MULTIPLIER = 1.8
AUDIO_FILE = "passive.wav"
RATE = 16000
CHUNK = 1024

# number of seconds to allow to establish threshold
THRESHOLD_TIME = 1

DELAY_MULTIPLIER = 1

# number of seconds to listen before forcing restart
LISTEN_TIME = 10


class Mic(object):

    def score_audio(self, data):
        """
        Returns the root-mean-square (power) of the audio signal.
        """

        rms = audioop.rms(data, 2)
        score = rms / 3
        return score

    def passive_listen(self, onset_utterance):
        """
        Listens for onset_utterance in everyday sound
        Times out after LISTEN_TIME, so needs to be restarted
        """

        # prepare recording stream
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        # stores the audio data
        frames = []

        # stores the last_n_scores score values
        last_n_scores = [i for i in range(30)]

        # calculate the long run average, and thereby the proper threshold
        for i in range(0, RATE / CHUNK * THRESHOLD_TIME):

            data = stream.read(CHUNK)
            frames.append(data)

            # save this data point as a score
            last_n_scores.pop(0)
            last_n_scores.append(self.score_audio(data))
            average = sum(last_n_scores) / len(last_n_scores)

        # this will be the benchmark to cause a disturbance over!
        local_threshold = average * THRESHOLD_MULTIPLIER

        # save some memory for sound data
        frames = []

        # flag raised when sound disturbance detected
        disturbance_detected = False

        # start passively listening for disturbance above threshold
        for i in range(0, RATE / CHUNK * LISTEN_TIME):

            data = stream.read(CHUNK)
            frames.append(data)
            score = self.score_audio(data)

            if score > local_threshold:
                disturbance_detected = True
                break

        # no use continuing if no flag raised
        if not disturbance_detected:
            return False

        # cutoff any recording before this disturbance was detected
        frames = frames[-20:]

        # otherwise, let's keep recording for few seconds and save the file

        for i in range(0, RATE / CHUNK * DELAY_MULTIPLIER):

            data = stream.read(CHUNK)
            frames.append(data)

        audio.terminate()

        print ''.join(frames)

        return True

        # # save the audio data
        # stream.stop_stream()
        # stream.close()
        # audio.terminate()
        # write_frames = wave.open(AUDIO_FILE, 'wb')
        # write_frames.setnchannels(1)
        # write_frames.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        # write_frames.setframerate(RATE)
        # write_frames.writeframes()
        # write_frames.close()

        # # check if onset_utterance was said
        # transcribed = self.transcribe(AUDIO_FILE, onset_utterance_ONLY=True)

        # if onset_utterance in transcribed:
        #     return (THRESHOLD, onset_utterance)

        # return (False, transcribed)

    def fetchThreshold(self):

        # TODO: Consolidate all of these variables from the next three
        # functions
        THRESHOLD_MULTIPLIER = 1.8
        RATE = 16000
        CHUNK = 1024

        # number of seconds to allow to establish threshold
        THRESHOLD_TIME = 1

        # prepare recording stream
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        # stores the audio data
        frames = []

        # stores the last_n_scores score values
        last_n_scores = [i for i in range(20)]

        # calculate the long run average, and thereby the proper threshold
        for i in range(0, RATE / CHUNK * THRESHOLD_TIME):

            data = stream.read(CHUNK)
            frames.append(data)

            # save this data point as a score
            last_n_scores.pop(0)
            last_n_scores.append(self.score_audio(data))
            average = sum(last_n_scores) / len(last_n_scores)

        # this will be the benchmark to cause a disturbance over!
        THRESHOLD = average * THRESHOLD_MULTIPLIER

        return THRESHOLD



    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        """
        Records until a second of silence or times out after 12 seconds
        """

        AUDIO_FILE = "active.wav"
        RATE = 16000
        CHUNK = 1024
        LISTEN_TIME = 12

        # user can request pre-recorded sound
        if not LISTEN:
            if not os.path.exists(AUDIO_FILE):
                return None

            return self.transcribe(AUDIO_FILE)

        # check if no threshold provided
        if THRESHOLD is None:
            THRESHOLD = self.fetchThreshold()

        self.voice.play_beep_high()

        # prepare recording stream
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        frames = []
        # increasing the range # results in longer pause after command
        # generation
        last_n_scores = [THRESHOLD * 1.2 for i in range(30)]

        for i in range(0, RATE / CHUNK * LISTEN_TIME):

            data = stream.read(CHUNK)
            frames.append(data)
            score = self.score_audio(data)

            last_n_scores.pop(0)
            last_n_scores.append(score)

            average = sum(last_n_scores) / float(len(last_n_scores))

            # TODO: 0.8 should not be a MAGIC NUMBER!
            if average < THRESHOLD * 0.8:
                break

        self.voice.play_beep_low()

        # save the audio data
        stream.stop_stream()
        stream.close()
        audio.terminate()
        write_frames = wave.open(AUDIO_FILE, 'wb')
        write_frames.setnchannels(1)
        write_frames.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        write_frames.setframerate(RATE)
        write_frames.writeframes(''.join(frames))
        write_frames.close()

        # DO SOME AMPLIFICATION
        # os.system("sox "+AUDIO_FILE+" temp.wav vol 20dB")

        if MUSIC:
            return self.transcribe(AUDIO_FILE, MUSIC=True)

        return self.transcribe(AUDIO_FILE)
