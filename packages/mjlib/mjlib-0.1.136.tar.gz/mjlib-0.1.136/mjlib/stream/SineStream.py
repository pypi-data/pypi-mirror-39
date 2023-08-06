import time
from numpy import *

from mjlib.stream import Stream


class SineStream(Stream):

    def x(self, sample):
        return sample[0]

    def y(self, sample):
        return sample[1]

    def __init__(self):
        super().__init__()
        self.i = 0.0

    def _get_sample(self):
        time.sleep(.005)  # sample rate = 200 like ganglion
        self.i = self.i + 0.03
        t = self.i
        sample = sin(2 * pi * t)
        return t, sample
