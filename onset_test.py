import logging

from otto.mic import OnsetMic
from otto.brain import Brain


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    m = OnsetMic()
    b = Brain()

    while True:
        frames = m.get_disturbance()
        hypothesis = b.transcribe(frames)
        if hypothesis[0]:
            logging.info('Heard "%s"', hypothesis[0])
