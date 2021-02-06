import signal
import time


class PanelController():

    def __init__(self):
        self.panels = list()
        self.is_active = True
        signal.signal(signal.SIGINT, self.handle_close_signal)
        signal.signal(signal.SIGTERM, self.handle_close_signal)

    def add_panel(self, panel):
        self.panels.append(panel)

    def wait(self):
        print('Press Ctrl+C to exit')
        while self.is_active:
            time.sleep(0.1)

    def close_all_panels(self):
        self.is_active = False
        for p in self.panels:
            p.close()

    def handle_close_signal(self, sig, frame):
        print("{0} received. Stopping threads.".format(signal.Signals(sig).name))
        self.close_all_panels()
