import os

# OTTO_PATH must be the root of the Otto project.
OTTO_PATH = os.path.normpath(
    os.path.join(os.path.realpath(os.path.dirname(__file__)), os.pardir))

LANGUAGE_FOLDER = os.path.join(OTTO_PATH, os.pardir, 'assets', 'language')
AUDIO_FOLDER = os.path.join(OTTO_PATH, os.pardir, 'assets', 'audio')

HMM_DIRECTORY = '/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k'
