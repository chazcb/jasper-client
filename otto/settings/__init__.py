import os
import yaml

# OTTO_PATH must be the root of the Otto project.
OTTO_PATH = os.path.normpath(os.path.join(os.path.realpath(os.path.dirname(__file__)), os.pardir))

LANGUAGE_FOLDER = os.path.join(OTTO_PATH, os.pardir, 'assets', 'language')
AUDIO_FOLDER = os.path.join(OTTO_PATH, os.pardir, 'assets', 'audio')
TMP_FOLDER = os.path.join(OTTO_PATH, os.pardir, 'assets', 'tmp')

USER_PROFILE = yaml.safe_load(open(os.path.join(OTTO_PATH, 'settings', 'profile.yml'), 'r'))

DEFAULT_LANGUAGE = 'default'
PERSONA_LANGUAGE = 'persona'
MUSIC_LANGUAGE = 'music'
