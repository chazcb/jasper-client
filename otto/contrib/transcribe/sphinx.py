try:
    import pocketsphinx as ps
except ValueError:
    import pocketsphinx as ps


# PocketSphinx requires specific framerate
# and sample width.
REQUIRED_FRAME_RATE = 16000
REQUIRED_SAMPLE_WIDTH = 2L
REQUIRED_N_CHANNELS = 1


class PocketSphinxSTT(object):

    def __init__(self):
        self.decoder = ps.Decoder(
            # lm='assets/language/onset.lm',
            # dict='assets/language/onset.dict',
            logfn='/dev/null',
        )

    def transcribe(self, wav):
        assert wav.getframerate() == REQUIRED_FRAME_RATE
        assert wav.getsamplewidth() == REQUIRED_SAMPLE_WIDTH
        assert wav.getnchannels() == REQUIRED_N_CHANNELS

        wav.seek(0)
        self.decoder.decode_raw(wav)
        wav.close()
        return self.decoder.get_hyp()[0]
