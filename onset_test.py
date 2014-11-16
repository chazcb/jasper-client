import logging

from otto.mic import OnsetMic
from otto.brain import Brain


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    m = OnsetMic()
    b = Brain()

    while True:
        onset_frames = m.get_disturbance()
        onset = b.transcribe(onset_frames)

        if 'computer' in onset[0].lower():
            phrase_frames = m.get_phrase()
            phrase = b.transcribe(phrase_frames)

            logging.info('Heard "%s"', phrase[0])
