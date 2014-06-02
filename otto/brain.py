from tempfile import TemporaryFile

try:
    import pocketsphinx as ps
except ValueError:
    import pocketsphinx as ps


# def play_file(file_path):
#     wf = wave.open(file_path, 'rb')

#     stream = audio.open(
#         format=audio.get_format_from_width(wf.getsampwidth()),
#         channels=wf.getnchannels(),
#         rate=wf.getframerate(),
#         output=True,
#     )

#     # read data
#     data = wf.readframes(CHUNK)

#     # play stream (3)
#     while data != '':
#         stream.write(data)
#         data = wf.readframes(CHUNK)

#     wf.close()
#     stream.stop_stream()
#     stream.close()


# def logError():
#     logger = logging.getLogger('jasper')
#     fh = logging.FileHandler('jasper.log')
#     fh.setLevel(logging.WARNING)
#     formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)
#     logger.error('Failed to execute module', exc_info=True)


class Brain(object):

    def __init__(self):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of modules. Note that the order of brain.modules
        matters, as the Brain will cease execution on the first module
        that accepts a given input.

        Arguments:
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
        """

        self.decoder = ps.Decoder(
            logfn='/dev/null'
        )

    def transcribe(self, data):
        tmp_file = TemporaryFile()
        tmp_file.writelines(data)
        tmp_file.seek(0)
        self.decoder.decode_raw(tmp_file)
        tmp_file.close()
        return self.decoder.get_hyp()

        # self.onset_decoder = ps.Decoder(
        #     lm='assets/language/onset.lm',
        #     dict='assets/language/onset.dict',
        # )

        # self.decoder = ps.Decoder()


        # self.mic = mic
        # self.profile = profile
        # self.modules = [
        #     Birthday,
        #     Gmail,
        #     Joke,
        #     Life,
        #     News,
        #     Notifications,
        #     Time,
        #     Weather,
        # ]
        # self.modules.append(Unclear)


    # def start_listening(self, onset_phrase):

    #     onset_frames = None
    #     phrase_frames = None

    #     # First, uppercase our onset phrase for consistency.
    #     onset_phrase = onset_phrase.upper()

    #     # Get local threshold
    #     local_threshold = self.get_local_threshold()
    #     play_file('assets/audio/beep_hi.wav')

    #     # Start a listener for audio frames above threshold
    #     onset_frames = self.listen_until(local_threshold)

    #     # If we got something above the threshold, let's check
    #     # to see if it contains our onset phrase.
    #     if onset_frames:
    #         onset_hyp = self.transcribe_with(onset_frames, self.onset_decoder)

    #         if onset_phrase in onset_hyp[0].upper():
    #             play_file('assets/audio/beep_hi.wav')
    #             phrase_frames = self.record_until(local_threshold)
    #             play_file('assets/audio/beep_lo.wav')

    #     if phrase_frames:
    #         return self.transcribe_with(phrase_frames, self.decoder)

    # def query(self, text):
    #     """
    #     Passes user input to the appropriate module, testing it against
    #     each candidate module's isValid function.

    #     Arguments:
    #     text -- user input, typically speech, to be parsed by a module
    #     """
    #     for module in self.modules:
    #         if module.isValid(text):

    #             try:
    #                 module.handle(text, self.mic, self.profile)
    #                 break
    #             except:
    #                 logError()
    #                 self.mic.voice.say(
    #                     "I'm sorry. I had some trouble with that operation. Please try again later.")
    #                 break
