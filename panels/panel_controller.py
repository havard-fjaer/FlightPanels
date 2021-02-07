import signal
import sys
import time
from threading import Thread


class PanelController():
    """
    Keeps the application alive, controls the panels, and terminates their threads on Ctrl-C.
    """

    def __init__(self):
        self.panels = list()
        self.is_active = True
        signal.signal(signal.SIGINT, self.handle_close_signal)
        signal.signal(signal.SIGTERM, self.handle_close_signal)

    def append(self, panel):
        panel.verbose = is_verbose()
        self.panels.append(panel)

    def start_all(self):
        for panel in self.panels:
            panel.connect()
            if panel.device_is_ready:
                Thread(target=panel.monitor_usb_device).start()
                Thread(target=panel.service.run).start()

    def wait(self):
        print('Press Ctrl+C to exit')
        while self.is_active:
            time.sleep(0.1)

    def close_all(self):
        self.is_active = False
        for p in self.panels:
            p.close()

    def handle_close_signal(self, sig, frame):
        print("{0} received. Stopping threads.".format(
            signal.Signals(sig).name))
        self.close_all()


def is_verbose():
    args = sys.argv[1:]
    return '-v' in args
