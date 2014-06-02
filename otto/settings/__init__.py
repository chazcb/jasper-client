import os

# OTTO_PATH must be the root of the Otto project.
OTTO_PATH = os.path.normpath(
    os.path.join(os.path.realpath(os.path.dirname(__file__)), os.pardir))

LANGUAGE_FOLDER = os.path.join(OTTO_PATH, os.pardir, 'assets', 'language')
AUDIO_FOLDER = os.path.join(OTTO_PATH, os.pardir, 'assets', 'audio')
TMP_FOLDER = os.path.join(OTTO_PATH, os.pardir, 'assets', 'tmp')

HMM_DIRECTORY = '/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k'

DEFAULT_MODEL_NAME = 'default'
PERSONA_MODEL_NAME = 'persona'
MUSIC_MODEL_NAME = 'music'

RATE = 16000
FRAMES_PER_BUFFER = 1024
FPS = RATE / FRAMES_PER_BUFFER

# Mic Settings
THRESHOLD_MULTIPLIER = 2.8

# number of seconds to listen before forcing restart
LISTEN_TIME = 10

# number of frames to average for threshold when checking if phrase has ended
LISTEN_SILENCE_TIMEOUT = 1.5
