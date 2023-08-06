from abc import abstractmethod, ABC


class Stream(ABC):
    def __init__(self):
        self._listeners = []

    def run(self):
        while True:
            sample = self._get_sample()
            if sample is None:
                break
            self._send(sample)

    @abstractmethod
    def _get_sample(self):
        pass

    def connect(self, output):
        if output not in self._listeners:
            self._listeners += output

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
