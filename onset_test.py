from otto.mic import OnsetMic
from otto.brain import Brain


if __name__ == "__main__":
    m = OnsetMic()
    b = Brain()

    frames = m.get_disturbance()
    print b.transcribe(frames)
