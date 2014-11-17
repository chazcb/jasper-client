from tempfile import TemporaryFile

try:
    import pocketsphinx as ps
except ValueError:
    import pocketsphinx as ps


class Brain(object):

    def __init__(self):
        """
        """

        self.decoder = ps.Decoder(
            # lm='assets/language/onset.lm',
            # dict='assets/language/onset.dict',
            logfn='/dev/null',
        )

    def transcribe(self, data):
        tmp_file = TemporaryFile()
        tmp_file.writelines(data)
        tmp_file.seek(0)
        self.decoder.decode_raw(tmp_file)
        tmp_file.close()
        return self.decoder.get_hyp()
