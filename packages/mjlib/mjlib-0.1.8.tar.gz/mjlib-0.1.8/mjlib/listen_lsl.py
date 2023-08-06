

from pylsl import resolve_stream, StreamInlet

import mjlib.config as config

# stream OpenBCI data from LSL to algorithm
def listen_lsl(main_win,cfg):
    print('listening to LSL')
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    print("receiving data")
    while True:
        sample, timestamp = inlet.pull_sample()
        print('sample: ' + str(sample))
        # sample = sample[0]

        # the zero problem only happened with OpenBCI
        # if sample != 0.0:

        if main_win.RESET_CHANNELS:
            config.reset_channels(*main_win.channel_reset_vars,main_win)
            main_win.RESET_CHANNELS = False

        # print('config.channels: ' + str(config.channels))

        for i in config.channels:
            main_win.data_in(sample[i],cfg,i)
