import os

from otto import settings
from otto import g2p

# quirky bug where first import doesn't work
try:
    from pocketsphinx import Decoder
except:
    from pocketsphinx import Decoder


class LanguageModel(object):

    def __init__(self, name):
        self.name = name
        self.language_model_file_path = os.path.join(settings.LANGUAGE_FOLDER, '%s_model.lm' % name)
        self.dictionary_file_path = os.path.join(settings.LANGUAGE_FOLDER, '%s_words.dict' % name)
        self.sentences_file_path = os.path.join(settings.LANGUAGE_FOLDER, '%s_sentences.txt' % name)

    @property
    def decoder(self):
        return Decoder(
            hmm=settings.HMM_DIRECTORY,
            m=self.language_model_file_path,
            dict=self.dictionary_file_path,
        )

    def build(self, words):

        # Create the dictionary
        pronounced = g2p.translateWords(words)

        lines = ["%s %s" % (x, y) for x, y in zip(words, pronounced)]

        with open(self.dictionary_file_path, "w") as f:
            f.write("\n".join(lines) + "\n")

        # Create the language model
        with open(self.sentences_file_path, "w") as f:
            f.write("\n".join(words) + "\n")
            f.write("<s> \n </s> \n")

        # Make language model
        os.system(
            "text2idngram -vocab {sentences_file_path} < {sentences_file_path} -idngram temp.idngram".format(
                sentences_file_path=self.sentences_file_path,
            )
        )

        os.system(
            "idngram2lm -idngram temp.idngram -vocab {sentences_file_path} -arpa {language_model_file_path}".format(
                sentences_file_path=self.sentences_file_path,
                language_model_file_path=self.language_model_file_path,
            )
        )
