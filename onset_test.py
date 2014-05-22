from otto.mic import Mic


m = Mic()


for _ in xrange(100):
    print _
    disturbance = m.passive_listen('computer')

    if disturbance:
        print disturbance
        break
