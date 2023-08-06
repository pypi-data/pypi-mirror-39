from abc import abstractmethod, ABC

streams = []


class Stream(ABC):
    def __init__(self):
        self._listeners = []
        self._coord_listeners = []
        self.open = True
        global streams
        streams.append(self)

    def run(self):
        print('running ' + str(self))
        while self.open:
            sample = self._get_sample()
            if sample is None:
                break
            coord = (self.x(sample), self.y(sample))
            self._send(sample, coord)

    def close(self):
        self.open = False

    @abstractmethod
    def _get_sample(self):
        pass

    @abstractmethod
    def x(self, sample):
        pass

    @abstractmethod
    def y(self, sample):
        pass

    def connect(self, output):
        if output not in self._listeners:
            self._listeners.append(output)

    def connect_coordinated(self, output):
        if output not in self._coord_listeners:
            self._coord_listeners.append(output)

    def disconnect(self, output):
        self._listeners -= output
        self._coord_listeners -= output

    def __iadd__(self, other):
        self.connect(other)
        return self

    def __add__(self, other):
        self.connect_coordinated(other)
        return self

    def __isub__(self, other):
        self.disconnect(other)
        return self

    def _send(self, sample, coord):
        for l in self._listeners:
            l(sample)
        for l in self._coord_listeners:
            l(coord)

    @staticmethod
    def shutdown():
        _close_all_streams()


def _close_all_streams():
    for s in streams:
        s.close()
