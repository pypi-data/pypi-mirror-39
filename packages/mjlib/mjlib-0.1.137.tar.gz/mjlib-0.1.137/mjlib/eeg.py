
channels = []

def reset_channels(a, b, c, main_win):
    channels.clear()

    if main_win.v_channel_1_on.get():
        channels.append(0)
    if main_win.v_channel_2_on.get():
        channels.append(1)
    if main_win.v_channel_3_on.get():
        channels.append(2)
    if main_win.v_channel_4_on.get():
        channels.append(3)
    if main_win.v_channel_5_on.get():
        channels.append(4)
    if main_win.v_channel_6_on.get():
        channels.append(5)
    if main_win.v_channel_7_on.get():
        channels.append(6)
    if main_win.v_channel_8_on.get():
        channels.append(7)


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
