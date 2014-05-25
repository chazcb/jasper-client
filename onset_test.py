from otto.mic import Mic


m = Mic()


if __name__ == "__main__":
    for _ in xrange(100):
        print _
        transcribed = m.start_listening('ok computer')

        if transcribed:
            print "*" * 20
            print transcribed
            print "*" * 20
