@property
def FREQ1(self):
    return self._FREQ1


@FREQ1.setter
def FREQ1(self, value):
    self._FREQ1 = value
    for callback in self._FREQ1_observers:
        callback(self._FREQ1)


def bind_to_FREQ1(self, callback):
    self._FREQ1_observers.append(callback)


# self._FREQ1 = 28.0  # 31.243
# self._FREQ1_observers = []




