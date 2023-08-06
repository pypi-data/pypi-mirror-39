import time
from numpy import *



# stream a generated sine wave to the algorithm for testing
def stream_sine(main_win,cfg):
    # print('cfg.plot4.5:' + str(cfg.plot))
    print("streaming sine")
    main_win.done_streaming = False
    i = 0.0
    while main_win.stream:
        # print('cfg.plot4.6:' + str(cfg.plot))
        time.sleep(.005)  # sample rate = 200 like ganglion
        i = i + 0.03
        t = i
        s = sin(2 * pi * t)
        main_win.data_in(s,cfg)
    main_win.done_streaming = True
    print("done streaming")
