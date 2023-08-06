import json

import os

print('PYTHONPATH:' + os.environ['PYTHONPATH'])
# matt_py_tools.
import mjlib.util as util

import mjlib.signal as signal

RAW = 1
TRANSFORMED = 2
CYTON = 1
GANGLION = 2
ENOBIO = 3

# Frequency Bands
DELTA = (0, 4)
THETA = (4, 7.5)
ALPHA_MU = (7.5, 12)
BETA = (16, 31)
GAMMA = (31, 100)


# container class for all parameters
# todo: serialize and deserialize from json
class Config():
    def __init__(self, j=None):
        super().__init__()

        self._FREQ1 = 28.0  # 31.243
        self._FREQ1_observers = []
        self._FREQ2 = 36.0  # 35.148
        self._FREQ2_observers = []
        self._FREQ3 = 41.45  # 41.627
        self._FREQ3_observers = []
        self._FREQ4 = 49.75  # 45.236
        self._FREQ4_observers = []

        self.DEVICE = ENOBIO

        self.GANGLION_Fs = 200
        self.CYTON_Fs = 250
        self.ENOBIO_Fs = 500
        if self.DEVICE is CYTON:
            self.Fs = self.CYTON_Fs
            self.extra_channels = 7
        elif self.DEVICE is GANGLION:
            self.Fs = self.GANGLION_Fs
            self.extra_channels = 3
        elif self.DEVICE is ENOBIO:
            self.Fs = self.ENOBIO_Fs
            self.extra_channels = 7

        # FFT_WIN = Fs * 8 # match openBCI according to processing code? but doesnt seem as responsive...
        # FFT_WIN = Fs * 2 # more responsive?
        # FFT_WIN = Fs * 1.5 # even more responsive... true openBCI value?
        # should be multiple of sample rate
        self.FFT_WIN = self.Fs * 5  # match experiment window length

        # set to 8 in java, set higher here because of cpu limitations
        self.FFT_OVERLAP = 64
        # self.FFT_OVERLAP = 16

        # max possible channels for any device
        self.MAX_CHANNELS = 8

        for i in range(self.MAX_CHANNELS):
            signal.fft_win.append([])

        self.N_LOOPS = None
        self.N_STIMS = 2
        self.REST_LENGTH = None
        self.TRIAL_LENGTH = None
        # self.N_TRIALS = None

        self.FileR = 0
        self.SNR_N_NEIGHBORS = 5
        self.SNR_PEAKS_N_NEIGHBORS = 2
        self.TRIPLE_DISPLAY = False

        self.LIVE_FFT_PLOT = True
        self.increment = 0.03
        self.SAMPLE = False
        self.SAMPLE_I = 1000
        self.ONE_STIM_TOGGLE = False
        self.FOUR_STIM = False
        self.LED_FEEDBACK = False
        self.DEBUG_FFT = False
        self.MULTI_CHANNEL = False
        self.LED_STIM = False
        self.CPP_ALGORITHM = False
        self.BAR_FEEDBACK = False
        self.USE_LSL = True
        self.LOG_FEEDBACK = False
        if not os.path.isdir("data"):
            os.mkdir('data')
        # '../../../data/feedback.log'
        self.FEEDBACK_LOG_FILE = 'data/feedback.log'
        util.clear_file(self.FEEDBACK_LOG_FILE)
        self.EXPERIMENT = False
        self.LABELS_LOG_FILE = 'data/labels.log'

        util.clear_file(self.LABELS_LOG_FILE)

        self.IS_RECORDING = False

        self.LOG_FILE_ALG_RESULTS = 'data/alg_results_channel.log'

        for i in [1, 2, 3, 4, 5, 6, 7, 8]:
            util.clear_file(self.LOG_FILE_ALG_RESULTS.replace('channel', str(i)))

        self.CHUNK_LENGTH = 15  # demofix_1 was 5
        self.POWER_LINE = 60.0
        self.F_START = 3
        self.F_STOP = 55

        if j is not None:
            self.__dict__ = json.loads(j)

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def FREQ1(self):
        return self._FREQ1

    @property
    def FREQ2(self):
        return self._FREQ2

    @property
    def FREQ3(self):
        return self._FREQ3

    @property
    def FREQ4(self):
        return self._FREQ4

    @FREQ1.setter
    def FREQ1(self, value):
        self._FREQ1 = value
        for callback in self._FREQ1_observers:
            callback(self._FREQ1)

    @FREQ2.setter
    def FREQ2(self, value):
        self._FREQ2 = value
        for callback in self._FREQ2_observers:
            callback(self._FREQ2)

    @FREQ3.setter
    def FREQ3(self, value):
        self._FREQ3 = value
        for callback in self._FREQ3_observers:
            callback(self._FREQ3)

    @FREQ4.setter
    def FREQ4(self, value):
        self._FREQ4 = value
        for callback in self._FREQ4_observers:
            callback(self._FREQ4)

    def bind_to_FREQ1(self, callback):
        self._FREQ1_observers.append(callback)

    def bind_to_FREQ2(self, callback):
        self._FREQ2_observers.append(callback)

    def bind_to_FREQ3(self, callback):
        self._FREQ3_observers.append(callback)

    def bind_to_FREQ4(self, callback):
        self._FREQ4_observers.append(callback)


cfg = Config()

channels = []
snrs_1 = []
snrs_2 = []


def reset_channels(a, b, c, main_win):
    channels.clear()
    snrs_1.clear()
    snrs_2.clear()

    if main_win.v_channel_1_on.get():
        channels.append(0)
        snrs_1.append(1)
        snrs_2.append(1)
    if main_win.v_channel_2_on.get():
        channels.append(1)
        snrs_1.append(1)
        snrs_2.append(1)
    if main_win.v_channel_3_on.get():
        channels.append(2)
        snrs_1.append(1)
        snrs_2.append(1)
    if main_win.v_channel_4_on.get():
        channels.append(3)
        snrs_1.append(1)
        snrs_2.append(1)
    if main_win.v_channel_5_on.get():
        channels.append(4)
        snrs_1.append(1)
        snrs_2.append(1)
    if main_win.v_channel_6_on.get():
        channels.append(5)
        snrs_1.append(1)
        snrs_2.append(1)
    if main_win.v_channel_7_on.get():
        channels.append(6)
        snrs_1.append(1)
        snrs_2.append(1)
    if main_win.v_channel_8_on.get():
        channels.append(7)
        snrs_1.append(1)
        snrs_2.append(1)
