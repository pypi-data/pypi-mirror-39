from abc import ABC

from pylsl import resolve_stream, StreamInlet

from mjlib.stream import Stream


class LSLStream(Stream, ABC):

    def __init__(self):
        super().__init__()
        streams = resolve_stream('type', 'EEG')
        self.inlet = StreamInlet(streams[0])

    def _get_sample(self):
        sample, timestamp = self.inlet.pull_sample()
        # sample = sample[0]

        # the zero problem only happened with OpenBCI
        # if sample != 0.0:

        return sample
