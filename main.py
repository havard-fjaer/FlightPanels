from panels.radio_panel import RadioPanel
from panels.radio_panel_flag import *
import signal
import sys
import threading
import time


def signal_handler(sig, frame):
    print("Signal '{0}' received. Stopping threads.".format(signal.Signals(sig).name))
    global stop
    stop = True


def is_verbose():
    args = sys.argv[1:]
    return '-v' in args

def main():
    global stop
    stop = False
    verbose = is_verbose()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    panel1 = RadioPanel(lambda: stop, verbose, usbBus=0, usbAddress=1)
    if panel1.device_is_ready:
        panel1.map_actions({
            RadioPanelButtonFlag.ENCODER_INNER_CW_1: lambda: print("Inner CW 1 - dev1"),
            RadioPanelButtonFlag.ENCODER_INNER_CCW_1: lambda: print("Inner CCW 1 - dev1"),
        })
        panel1.set_lcd(RadioPanelLcd.LCD1, "12345678900987654321")
    else:
        print("Failed to load device.")

    panel2 = RadioPanel(lambda: stop, verbose, usbBus=0, usbAddress=2)
    if panel2.device_is_ready:
        panel2.map_actions({
            RadioPanelButtonFlag.ENCODER_INNER_CW_1: lambda: panel2.set_lcd(RadioPanelLcd.LCD1, "11111111111111111111"),
            RadioPanelButtonFlag.ENCODER_INNER_CCW_1: lambda: panel2.set_lcd(RadioPanelLcd.LCD1, "22222222222222222222"),
        })
        panel2.set_lcd(RadioPanelLcd.LCD1, "12345678900987654321")
    else:
        print("Failed to load device.")

    print('Press Ctrl+C to exit')
    while not stop:
        time.sleep(0.1)
        if threading.active_count() <= 1:
            print("All devices disconnected.")
            stop = True


if __name__ == "__main__":
    main()
