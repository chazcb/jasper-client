from otto.mic import Mic
from otto.brain import Brain


if __name__ == "__main__":
    m = Mic()
    b = Brain()

    frames, _ = m.get_disturbance()
    print b.transcribe(frames)
