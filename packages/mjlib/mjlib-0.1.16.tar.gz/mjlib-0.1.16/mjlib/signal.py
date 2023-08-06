

from scipy.signal import *
from numpy.fft import *


from pathlib import Path
parent = Path(str(__file__)).parent
# import util
import importlib.util
spec = importlib.util.spec_from_file_location("util", str(parent) + "/util.py")
util = importlib.util.module_from_spec(spec)
spec.loader.exec_module(util)
# foo.MyClass()


fft_win = []

class Config:
    def __init__(self):
        self.Fs = 1

        # should be multiple of sample rate
        self.FFT_WIN = self.Fs * 5

# bandpass filter for eeg data
def bandpass(data, low, high,cfg):
    nyq = 0.5 * cfg.Fs
    # noinspection PyTupleAssignmentBalance
    b2, a2 = butter(5, [low / nyq, high / nyq], btype='band')
    r = lfilter(b2, a2, data)
    return r

# bandstop filter for eeg data
def bandstop(data, f, w,cfg):
    nyq = 0.5 * cfg.Fs
    low = f - w / 2
    high = f + w / 2
    # noinspection PyTupleAssignmentBalance
    b2, a2 = butter(5, [low / nyq, high / nyq], 'bandstop')
    r = lfilter(b2, a2, data)
    return r

# calculate the single-sided power spectrum from the two-sided power spectrum
def p1(P2):
    # prof('p1')
    p1 = []
    i = 0
    for p in P2:
        if i < int(len(P2) / 2) + 1:
            p1.append(p)
        i = i + 1
    for n in range(1, len(p1) - 2):
        p1[n] = p1[n] * 2
    return p1


# get the single-sided power spectrum of a window of EEG data
def ps(data,cfg):
    # prof('fft')
    Y = fft(data)
    P2 = p2(Y,cfg)
    P1 = p1(P2)
    freqs = p1_freqs(len(P2), cfg.Fs)
    return P1, freqs



# calculate the freqeuncy bins of an fft of data with window length L and sample rate Fs
def p1_freqs(L, Fs):
    # actualy, I just probably had Fs wrong again
    # this doesnt work right, just do it the matlab way

    l = list(range(0, int(L / 2) + 1))
    ll = [x / L for x in l]
    freqs = [x * Fs for x in ll]

    return freqs


# two-sided fft power spectrum for eeg data
def p2(Y,cfg):
    # prof('p2')
    return abs(Y / cfg.FFT_WIN)


