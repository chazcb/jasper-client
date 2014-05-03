
import os
import modules

from otto import settings
from otto import g2p


class LanguageAssets(object):

    def __init__(self, name):
        self.name = name
        self.language_model_file_path = os.path.join(settings.LANGUAGE_FOLDER, '%s_model.lm' % name)
        self.dictionary_file_path = os.path.join(settings.LANGUAGE_FOLDER, '%s_words.dict' % name)
        self.sentences_file_path = os.path.join(settings.LANGUAGE_FOLDER, '%s_sentences.txt' % name)

    def rebuild(self, words):

        # create the dictionary
        pronounced = g2p.translateWords(words)

        lines = ["%s %s" % (x, y) for x, y in zip(words, pronounced)]

        with open(self.dictionary_file_path, "w") as f:
            f.write("\n".join(lines) + "\n")

        # create the language model
        with open(self.sentences_file_path, "w") as f:
            f.write("\n".join(words) + "\n")
            f.write("<s> \n </s> \n")

        # make language model
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


def compile_all():
    """
    This iterates over all the WORDS variables in the modules and
    creates a dictionary that the client program will use.
    """

    m = dir(modules)

    words = []
    for module_name in m:
        try:
            eval('words.extend(modules.%s.WORDS)' % module_name)
        except:
            pass  # module probably doesn't have the property

    words = list(set(words))

    # for spotify module
    words.extend(['MUSIC', 'SPOTIFY'])

    default_assets = LanguageAssets('default', words)
    default_assets.build()
