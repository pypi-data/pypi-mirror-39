from tkinter import Variable


class Prop:
    def __init__(self, initialValue=None, callback=None):
        self._var = Variable(value=initialValue)
        if callback is not None:
            self._var.trace(mode='w', callback=callback)

    def get(self):
        return self._var.get()

    def set(self, value):
        self._var.set(value)


class IntProp(Prop):
    def __init__(self, initialValue=0, callback=None):
        super().__init__(initialValue, callback)


class StringProp(Prop):
    def __init__(self, initialValue="", callback=None):
        super().__init__(initialValue, callback)


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
