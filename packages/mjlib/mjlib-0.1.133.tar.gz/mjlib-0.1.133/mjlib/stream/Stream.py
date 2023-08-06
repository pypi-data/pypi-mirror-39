from abc import abstractmethod, ABC

streams = []


class Stream(ABC):
    def __init__(self):
        self._listeners = []
        self.open = True
        global streams
        streams += self

    def run(self):
        print('running ' + str(self))
        while self.open:
            sample = self._get_sample()
            if sample is None:
                break
            self._send(sample)

    def close(self):
        self.open = False

    @abstractmethod
    def _get_sample(self):
        pass

    def connect(self, output):
        if output not in self._listeners:
            self._listeners.append(output)

    def disconnect(self, output):
        self._listeners -= output

    def __iadd__(self, other):
        self.connect(other)
        return self

    def __isub__(self, other):
        self.disconnect(other)
        return self

    def _send(self, sample):
        for l in self._listeners:
            l(sample)

    @staticmethod
    def shutdown():
        _close_all_streams()


def _close_all_streams():
    for s in streams:
        s.close()
