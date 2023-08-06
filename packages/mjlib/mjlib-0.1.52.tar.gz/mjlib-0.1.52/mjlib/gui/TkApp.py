from abc import ABC, abstractmethod
import sys
import warnings
from time import sleep


class TkApp(ABC):

    def __init__(self, root, topmost=False):
        root.update()

        if topmost:
            root.call('wm', 'attributes', '.', '-topmost', '1')

        root.wm_title(self.__class__.__name__)

        def on_closing():
            self.on_quit()
            root.destroy()
            sys.exit(0)
        root.protocol("WM_DELETE_WINDOW", on_closing)

        self.live_plots = []

        self.start()
        root.after(0, self._animate, root)
        self._enter_event_loop(root)

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def on_quit(self):
        pass

    @abstractmethod
    def animate(self):
        pass

    def _animate(self,root):
        try:
            sleep(0.05)
            for lp in self.live_plots:
                lp.animate()
            self.animate()
            root.after(50, self._animate,root)
        except KeyboardInterrupt as e:
            print('exiting from KeyboardInterrupt')
            sys.exit(0)

    def _enter_event_loop(self, root):
        try:
            # https://stackoverflow.com/questions/16995969/inertial-scrolling-in-mac-os-x-with-tkinter-and-python
            while True:
                try:
                    # prevent: RuntimeWarning: internal gelsd driver lwork query error
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        root.mainloop()
                    break
                except UnicodeDecodeError:
                    pass
                except SystemExit as e:
                    if not root:  # no idea if this works
                        root.destroy()
                    sys.exit(e.code)
        except KeyboardInterrupt as e:
            print('exiting as a result of ' + str(e))
            sys.exit(0)
