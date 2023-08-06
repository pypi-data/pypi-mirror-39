import matplotlib
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import *
import numpy as np
from pynput.mouse import Controller
from scipy.io import *
from tkinter import N, S, E, W, filedialog
import sys
import warnings

import mjlib.config as config
import mjlib.listen_lsl
import mjlib.util as util
# from matt_tools.exp import run_experiment
from mjlib.listen_sine import stream_sine
from mjlib.listen_udp import udp_socket

main_win = None


# main class for GUI, controls, and live plot
class AppWindow(tk.Tk):
    def __init__(self, parent, cfg, data_inputs,collect_script):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.data_inputs = data_inputs

        self.cfg = cfg

        self.collect_script = collect_script

        self.stream = False
        self.done_streaming = True
        self.RAW_WIN = 100
        self.raw_win = np.zeros((self.RAW_WIN, 8))
        self.RAW_WIN_X = range(self.RAW_WIN)

        print('initializing app window')
        self.initialize()
        print('initialized app window')

        # for macbook display
        self.wm_geometry("1200x750+0+0")  # only size matters here since we

        if self.cfg.TRIPLE_DISPLAY:
            self.wm_geometry("800x925+0+0")  # only size matters here since we center after
            self.center()  # move to good spot on monitor

        x = 300
        y = 0

        self.y = []

    def center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def initialize(self):

        Fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        self.FigSubPlot = Fig.add_subplot(111)
        self.FigSubPlot.axes.get_xaxis().set_visible(False)
        x = []
        y = []
        self.line1, = self.FigSubPlot.plot(x, y, 'r-')
        self.line2, = self.FigSubPlot.plot(x, y, 'y-')
        self.line3, = self.FigSubPlot.plot(x, y, 'g-')
        self.line4, = self.FigSubPlot.plot(x, y, 'b-')
        self.line5, = self.FigSubPlot.plot(x, y, 'r--')
        self.line6, = self.FigSubPlot.plot(x, y, 'y--')
        self.line7, = self.FigSubPlot.plot(x, y, 'g--')
        self.line8, = self.FigSubPlot.plot(x, y, 'b--')
        self.lines = [self.line1, self.line2, self.line3, self.line4, self.line5, self.line6, self.line7, self.line8]
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(Fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=10,
                                         sticky=N + S + W + E)

        self.stim_feedback_canv = tk.Canvas(self, width=130, height=200, bg="white")
        self.circ_1 = self.stim_feedback_canv.create_oval(20, 70, 120, 170)
        self.stim_feedback_canv.create_text(70, 120, text="28Hz")
        self.circ_2 = self.stim_feedback_canv.create_oval(20, 270, 120, 370, fill="yellow")
        self.stim_feedback_canv.create_text(70, 320, text="36Hz")
        self.stim_feedback_canv.grid(row=0, column=9, sticky=W + N + S + E, columnspan=2)

        next_canvas = tk.Canvas(self, width=128, height=20, bg="white")
        line = next_canvas.create_line(0, 25, 2000, 25)

        next_canvas.grid(row=1, column=0, columnspan=100, sticky=N + S + E + W)

        r = 2

        self.v_source = tk.IntVar()

        tk.Label(self, text="Source:").grid(row=r, column=0)
        tk.Radiobutton(self, text="Ganglion", variable=self.v_source, value=1, command=self.on_switch_source).grid(
            row=r, column=1)
        tk.Radiobutton(self, text="Cyton", variable=self.v_source, value=2, command=self.on_switch_source).grid(row=r,
                                                                                                                column=2)
        tk.Radiobutton(self, text="Enobio", variable=self.v_source, value=6, command=self.on_switch_source).grid(row=r,
                                                                                                                 column=3)
        tk.Radiobutton(self, text="Noise", variable=self.v_source, value=3, command=self.on_switch_source).grid(row=r,
                                                                                                                column=4)
        tk.Radiobutton(self, text="Sine", variable=self.v_source, value=4, command=self.on_switch_source).grid(row=r,
                                                                                                               column=5)
        tk.Radiobutton(self, text="Recording", variable=self.v_source, value=5, command=self.on_switch_source).grid(
            row=r, column=6)

        self.v_network = tk.StringVar(self)
        tk.OptionMenu(self, self.v_network, "UDP", "LSL").grid(row=r, column=7)
        r = r + 1
        tk.Label(self, text="Channels:").grid(row=r, column=0)
        self.v_channel_1_on = tk.IntVar()
        self.v_channel_2_on = tk.IntVar()
        self.v_channel_3_on = tk.IntVar()
        self.v_channel_4_on = tk.IntVar()
        self.v_channel_5_on = tk.IntVar()
        self.v_channel_6_on = tk.IntVar()
        self.v_channel_7_on = tk.IntVar()
        self.v_channel_8_on = tk.IntVar()

        self.RESET_CHANNELS = False
        self.channel_reset_vars = None

        def on_change_channels(a, b, c):
            self.channel_reset_vars = (a, b, c)
            self.RESET_CHANNELS = True

        self.v_channel_1_on.trace(mode="w", callback=on_change_channels)
        self.v_channel_2_on.trace(mode="w", callback=on_change_channels)
        self.v_channel_3_on.trace(mode="w", callback=on_change_channels)
        self.v_channel_4_on.trace(mode="w", callback=on_change_channels)
        self.v_channel_5_on.trace(mode="w", callback=on_change_channels)
        self.v_channel_6_on.trace(mode="w", callback=on_change_channels)
        self.v_channel_7_on.trace(mode="w", callback=on_change_channels)
        self.v_channel_8_on.trace(mode="w", callback=on_change_channels)

        self.winner = 1

        tk.Checkbutton(self, text="1", onvalue=1, offvalue=0, variable=self.v_channel_1_on).grid(row=r, column=1)
        tk.Checkbutton(self, text="2", onvalue=1, offvalue=0, variable=self.v_channel_2_on).grid(row=r, column=2)
        tk.Checkbutton(self, text="3", onvalue=1, offvalue=0, variable=self.v_channel_3_on).grid(row=r, column=3)
        tk.Checkbutton(self, text="4", onvalue=1, offvalue=0, variable=self.v_channel_4_on).grid(row=r, column=4)
        self.channel_5_box = tk.Checkbutton(self, text="5", onvalue=1, offvalue=0, variable=self.v_channel_5_on)
        self.channel_5_box.grid(row=r, column=5)
        self.channel_6_box = tk.Checkbutton(self, text="6", onvalue=1, offvalue=0, variable=self.v_channel_6_on)
        self.channel_6_box.grid(row=r, column=6)
        self.channel_7_box = tk.Checkbutton(self, text="7", onvalue=1, offvalue=0, variable=self.v_channel_7_on)
        self.channel_7_box.grid(row=r, column=7)
        self.channel_8_box = tk.Checkbutton(self, text="8", onvalue=1, offvalue=0, variable=self.v_channel_8_on)
        self.channel_8_box.grid(row=r, column=8)
        r = r + 1
        tk.Label(self, text="Pre-Processing:").grid(row=r, column=0)
        tk.Checkbutton(self, text="bandstop").grid(row=r, column=1)
        tk.Checkbutton(self, text="bandpass").grid(row=r, column=2)
        tk.Checkbutton(self, text="detrend").grid(row=r, column=3)
        r = r + 1
        tk.Label(self, text="Transform:").grid(row=r, column=0)
        v_transform = tk.IntVar()
        tk.Radiobutton(self, text="FFT", variable=v_transform, value=1).grid(row=r,
                                                                             column=1)
        tk.Radiobutton(self, text="PWelch", variable=v_transform, value=2).grid(row=r,
                                                                                column=2)
        tk.Label(self, text="window(s):").grid(row=r, column=3)
        scl = tk.Scale(self, from_=1, to_=10, orient=tk.HORIZONTAL)
        scl.grid(row=r, column=4)
        scl.set(5)
        r = r + 1
        tk.Label(self, text="Classification:").grid(row=r, column=0)
        r = r + 1
        tk.Label(self, text="Feedback:").grid(row=r, column=0)
        self.v_feedback_LED = tk.IntVar()
        tk.Checkbutton(self, text="LED", onvalue=1, offvalue=0, variable=self.v_feedback_LED).grid(row=r, column=1)
        r = r + 1
        tk.Label(self, text="Plot:").grid(row=r, column=0)
        self.v_plot = tk.IntVar()
        self.v_ymax = tk.StringVar()
        self.v_ymin = tk.StringVar()
        v_xmax = tk.StringVar()
        self.reset_x = False

        self.line1 = None
        self.line2 = None

        tk.Radiobutton(self, text="raw", variable=self.v_plot, value=config.RAW, command=self.on_change_plot).grid(
            row=r,
            column=1)
        tk.Radiobutton(self, text="transformed", variable=self.v_plot, value=config.TRANSFORMED,
                       command=self.on_change_plot).grid(row=r, column=2)
        v_shake = tk.IntVar()

        self.mouse = Controller()
        keep_moving_mouse = False
        done_moving_mouse = True

        def on_change_shake(a, b, c):
            if v_shake.get():
                self.keep_moving_mouse = True
                util.daemon(self.mouse_mover)
            else:
                self.keep_moving_mouse = False

        v_shake.trace_variable(mode="w", callback=on_change_shake)
        tk.Checkbutton(self, text="shake", onvalue=1, offvalue=0, variable=v_shake).grid(row=r, column=3)


        self.v_ymax.trace_variable(mode="w", callback=self.on_change_ymax)
        self.v_ymin.trace_variable(mode="w", callback=self.on_change_ymax)

        tk.Label(self, text="ymin:").grid(row=r, column=4)
        entry = tk.Entry(self, textvariable=self.v_ymin, width=10)
        entry.grid(row=r, column=5)
        self.v_ymax.set("100")

        tk.Label(self, text="ymax:").grid(row=r, column=6)
        entry = tk.Entry(self, textvariable=self.v_ymax, width=10)
        entry.grid(row=r, column=7)
        self.v_ymax.set("100")


        tk.Label(self, text="xmax:").grid(row=r, column=8)

        v_xmax.trace_variable(mode="w", callback=self.on_change_xmax)
        entry = tk.Entry(self, textvariable=v_xmax, width=10)
        entry.grid(row=r, column=9)
        # self.v_ymax.set("100")

        r = r + 1
        tk.Label(self, text="Record:").grid(row=r, column=0)
        tk.Label(self, text="freqs:").grid(row=r, column=1)
        self.v_freq_from = tk.StringVar()
        self.v_freq_step = tk.StringVar()
        self.v_freq_to = tk.StringVar()
        tk.Spinbox(self, width=5, from_=0, to_=60, textvariable=self.v_freq_from).grid(row=r, column=2)
        tk.Label(self, text=":").grid(row=r, column=3)
        tk.Spinbox(self, width=5, from_=0, to_=5, textvariable=self.v_freq_step).grid(row=r, column=4)
        tk.Label(self, text=":").grid(row=r, column=5)
        tk.Spinbox(self, width=5, from_=0, to_=60, textvariable=self.v_freq_to).grid(row=r, column=6)
        tk.Label(self, text="trial:").grid(row=r, column=7)
        self.v_trial = tk.StringVar()
        tk.Spinbox(self, width=5, from_=5, to_=30, textvariable=self.v_trial).grid(row=r, column=8)
        tk.Label(self, text="rest:").grid(row=r, column=9)
        self.v_rest = tk.StringVar()
        tk.Spinbox(self, width=5, from_=5, to_=10, textvariable=self.v_rest).grid(row=r, column=10)

        tk.Label(self, text="loops:").grid(row=r, column=11)
        self.v_loops = tk.StringVar()
        tk.Spinbox(self, width=5, from_=1, to_=5, textvariable=self.v_loops).grid(row=r, column=12)

        def on_collect():
           self.collect_script(self)

        tk.Button(self, text="collect", command=on_collect).grid(row=r, column=13),
        r = r + 1
        tk.Label(self, text="Test:").grid(row=r, column=0)

        def on_quick_check():
            eeg = loadmat('/Users/matt/Desktop/registered/todo/eeg_analysis_pipeline/quick_data.mat')
            eeg = eeg['eeg']
            old_eeg = eeg
            eeg = []
            for e in old_eeg:
                eeg.append(e[0])

            def get_eeg():
                l = len(eeg)
                for i, e in enumerate(eeg):
                    print('quick eeg in (' + str(i) + '/' + str(l) + ')')
                    data_in(e, cfg)

            util.daemon(get_eeg)

        tk.Button(self, text="quick check", command=on_quick_check).grid(row=r, column=1, columnspan=2),
        r = r + 1
        tk.Label(self, text="NFB:").grid(row=r, column=0)
        v_nfb = tk.IntVar()
        tk.Radiobutton(self, text="delta", variable=v_nfb, value=1).grid(row=r, column=1)
        tk.Radiobutton(self, text="theta", variable=v_nfb, value=2).grid(row=r, column=2)
        tk.Radiobutton(self, text="alpha/mu", variable=v_nfb, value=3).grid(row=r, column=3)
        tk.Radiobutton(self, text="beta", variable=v_nfb, value=4).grid(row=r, column=4)
        tk.Radiobutton(self, text="gamma", variable=v_nfb, value=5).grid(row=r, column=5)
        self.v_threshold = tk.StringVar()
        tk.Label(self, text="threshold:").grid(row=r, column=6)
        entry = tk.Entry(self, textvariable=self.v_threshold, width=10)
        entry.grid(row=r, column=7)
        self.v_positive = tk.IntVar()
        tk.Checkbutton(self, text="positive", onvalue=1, offvalue=0, variable=self.v_positive).grid(row=r, column=8)
        r = r + 1
        tk.Button(self, text="Load Config", command=self.on_load_cfg).grid(row=r, column=0)
        tk.Button(self, text="Save Config", command=self.on_save_cfg).grid(row=r, column=1, columnspan=2)
        r = r + 1
        tk.Label(self, text="Debug:").grid(row=r, column=0)
        tk.Button(self, text="Profile", command=self.on_click_profile).grid(row=r, column=1)

        r = r + 1

        self.status_label = tk.Label(self, text="")
        self.status_label.grid(row=r, column=0, columnspan=100)

        for i in range(8 + 1):
            tk.Grid.columnconfigure(self, i, weight=1)
        for i in range(r + 1):
            tk.Grid.rowconfigure(self, i, weight=1)

        print('setting app window resizable')
        self.resizable(False, False)

        self.fig_x = []
        self.fig_y = [[], [], [], [], [], [], [], []]  # each channel

    def animate(self):
        try:
            time.sleep(0.05)
            for c in range(len(self.fig_y)):
                l = len(self.fig_y[c])
                if l > 0:
                    self.lines[c].set_data(self.fig_x, self.fig_y[c])
            if self.reset_x:
                if len(self.fig_x) > 0:
                    self.canvas.figure.axes[0].set_xlim(min(self.fig_x), max(self.fig_x))
                    self.reset_x = False

            if self.winner is 1:
                self.stim_feedback_canv.itemconfigure(self.circ_2, fill="white")
                self.stim_feedback_canv.itemconfigure(self.circ_1, fill="yellow")
            elif self.winner is 2:
                self.stim_feedback_canv.itemconfigure(self.circ_2, fill="yellow")
                self.stim_feedback_canv.itemconfigure(self.circ_1, fill="white")

            self.canvas.draw()
            self.after(50, self.animate)
        except KeyboardInterrupt as e:
            print('exiting from KeyboardInterrupt')
            sys.exit(0)

    def on_save_cfg(self):
        file = filedialog.asksaveasfilename(
            initialdir=os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir, 'configs')),
            filetypes=(("json files", "*.json"),), title="Select where to save config file")
        if not ".json" in str(file):
            file = str(file) + ".json"
        j = cfg.to_json()
        with open(file, "w") as myfile:
            myfile.write(j)

    def on_load_cfg(self):
        file = filedialog.askopenfilename(
            initialdir=os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, os.pardir, 'configs')),
            filetypes=(("json files", "*.json"),), title="Select config file to load")

        with open(file) as f:
            j = f.readlines()
        config.cfg = config.Config(j)

    def data_in(self, e, cfg, c=0):

        util.prof('eeg_in')

        # print('not plotting...?')
        # print('cfg.plot5:' + str(cfg.plot))
        # print('self.stream:' + str(self.stream))
        if cfg.plot is config.RAW and self.stream:
            # print('updating chart?: ' + str(e))
            temp_c_win = list(self.raw_win[:, c])
            del temp_c_win[0]
            temp_c_win.append(e)
            self.raw_win[:, c] = temp_c_win
            self.fig_x = self.RAW_WIN_X
            self.fig_y[c] = temp_c_win

        for inp in self.data_inputs:
            inp(e, self, cfg, c)

    def on_switch_source(self):
        print("switched source: " + str(self.v_source.get()))
        stream = False
        while not self.done_streaming:
            time.sleep(0.01)
        self.stream = True
        if self.v_source.get() is 4:
            print("switching to source: sine")
            util.daemon(stream_sine, args=(self, cfg))
        elif self.v_source.get() is 1 or self.v_source.get() is 2 or self.v_source.get() is 6:
            if self.v_source.get() is 1:
                cfg.Fs = cfg.GANGLION_Fs
                self.channel_5_box.config(state='disabled')
                self.channel_6_box.config(state='disabled')
                self.channel_7_box.config(state='disabled')
                self.channel_8_box.config(state='disabled')
            elif self.v_source.get() is 2:
                cfg.Fs = cfg.CYTON_Fs
            elif self.v_source.get() is 6:
                cfg.Fs = cfg.ENOBIO_Fs
            print("switching to source: udp")
            global main_win
            if self.v_network.get() == "UDP":
                util.daemon(udp_socket, args=(main_win, cfg))
            elif self.v_network.get() == "LSL":
                print('starting listen_lsl thread')
                util.daemon(listen_lsl.listen_lsl, args=(main_win, cfg))
            else:
                print("Pick a network type to stream live data!")
        print("done switching source")

    def on_change_plot(self):
        config.cfg.plot = self.v_plot.get()

        self.FigSubPlot.axes.get_xaxis().set_visible(self.v_plot.get() is config.TRANSFORMED)

        if self.v_plot.get() is config.TRANSFORMED:
            self.line1 = self.FigSubPlot.axes.axvline(x=config.cfg.FREQ1, linewidth=2, color='grey')

            self.line2 = self.FigSubPlot.axes.axvline(x=config.cfg.FREQ2, linewidth=2, color='grey')
        elif self.line1 is not None:
            self.FigSubPlot.axes.lines.remove(self.line1)
            self.FigSubPlot.axes.lines.remove(self.line2)

        self.on_change_ymax(None, None, None)

        self.reset_x = True

    def on_change_ymax(self, a, b, c):
        try:
            if self.v_plot.get() is config.TRANSFORMED:
                self.FigSubPlot.axes.set_ylim(int(self.v_ymin.get()), int(self.v_ymax.get()))

            else:
                self.FigSubPlot.axes.set_ylim(int(self.v_ymin.get()), int(self.v_ymax.get()))
        except ValueError:
            pass


    def on_change_xmax(self, a, b, c):
        try:
            self.FigSubPlot.axes.set_xlim(0, int(v_xmax.get()))
        except ValueError:
            pass

    def on_click_profile(self):

        vars.is_profiling = True
        print('self.is_profiling =', str(vars.is_profiling))

    def mouse_mover():
        l = True
        while keep_moving_mouse:
            time.sleep(.01)
            if l:
                mouse.move(0, -1)
            else:
                mouse.move(0, 1)
            l = not l
        done_moving_mouse = False


def start_app(main_win,title, cfg,test_plot=True):

    try:

        # print('cfg.plot2:' + str(cfg.plot))
        print('updating app win')
        main_win.update()

        # main_win.lift()
        main_win.call('wm', 'attributes', '.', '-topmost', '1')

        print('putting title on app window')
        main_win.wm_title(title)
        print('created app window and put title')

        # https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
        def on_closing():
            main_win.destroy()
            sys.exit(0)

        main_win.protocol("WM_DELETE_WINDOW", on_closing)

        main_win.after(0, main_win.animate())

        def test():

            main_win.stream = True
            cfg.plot = config.RAW
            main_win.v_source.set(4)
            main_win.v_plot.set(1)
            main_win.v_ymax.set(10)
            main_win.on_change_plot()
            # print('cfg.plot4:' + str(cfg.plot))
            util.daemon(stream_sine, args=(main_win, cfg))
            print('here, should be testing...')
        # print('cfg.plot3:' + str(cfg.plot))
        if test_plot:
            util.daemon(test)

        # https://stackoverflow.com/questions/16995969/inertial-scrolling-in-mac-os-x-with-tkinter-and-python
        while True:
            try:
                # prevent: RuntimeWarning: internal gelsd driver lwork query error, required iwork dimension not returned. This is likely the result of LAPACK bug 0038, fixed in LAPACK 3.2.2 (released July 21, 2010). Falling back to 'gelss' driver.
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    main_win.mainloop()
                break
            except UnicodeDecodeError:
                pass
            except SystemExit as e:
                if not main_win: # no idea if this works
                    main_win.destroy()
                sys.exit(e.code)
        return main_win
    except KeyboardInterrupt as e:
        print('exiting from ' + str(e))
        sys.exit(0)