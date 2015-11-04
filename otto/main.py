# import wit
# from otto import settings
import pyaudio

try:
    import pocketsphinx as ps
except ValueError:
    import pocketsphinx as ps


# PocketSphinx requires specific framerate
# and sample width.
REQUIRED_FRAME_RATE = 16000
REQUIRED_SAMPLE_WIDTH = 2L
REQUIRED_N_CHANNELS = 1

# Create a decoder with certain model
config = ps.Decoder.default_config()
# config.set_string('-hmm', os.path.join(modeldir, 'hmm/en_US/hub4wsj_sc_8k'))
# config.set_string('-dict', os.path.join(modeldir, 'lm/en_US/cmu07a.dic'))
config.set_string('-keyphrase', 'forward')
config.set_float('-kws_threshold', 1e-20)





# Open file to read the data
# stream = open(os.path.join(datadir, "goforward.raw"))

# Alternatively you can read from microphone
# import pyaudio
#
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

# # Process audio chunk by chunk. On keyword detected perform action and restart search

# class PocketSphinxSTT(object):

#     def __init__(self):
#         self.decoder = ps.Decoder(
#             # lm='assets/language/onset.lm',
#             # dict='assets/language/onset.dict',
#             logfn='/dev/null',
#         )

#     def transcribe(self, wav):
#         assert wav.getframerate() == REQUIRED_FRAME_RATE
#         assert wav.getsamplewidth() == REQUIRED_SAMPLE_WIDTH
#         assert wav.getnchannels() == REQUIRED_N_CHANNELS

#         wav.seek(0)
#         self.decoder.decode_raw(wav)
#         wav.close()
#         return self.decoder.get_hyp()[0]


if __name__ == 'main':
    # wit.init()

    decoder = ps.Decoder(config)
    decoder.start_utt('spotting')
    while True:
        buf = stream.read(1024)
        if not buf:
            break
        decoder.process_raw(buf, False, False)
        if decoder.hyp() is not None and decoder.hyp().hypstr == 'forward':
            print "Heard '%s'." % decoder.hyp().hypstr
            print "DETECTED: Detected keyword, restarting search."
        decoder.end_utt()
        decoder.start_utt('spotting')
