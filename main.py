from panels.radio_panel import RadioPanel
from panels.radio_panel_flag import RadioPanelButtonFlag
from panels.panel_text_converter import PanelTextConverter
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

    actionMapping1 = {
        RadioPanelButtonFlag.ENCODER_INNER_CW_1: lambda: print("Inner CW 1"),
        RadioPanelButtonFlag.ENCODER_INNER_CCW_1: lambda: print("Inner CCW 1"),
    }

    print(actionMapping1)

    panel1 = RadioPanel(lambda: stop, verbose, actionMapping1, usbBus=0, usbAddress=1)
    panel1.connect()
    lcd = PanelTextConverter()
    panel1.print_message(lcd.convert_string_to_bytes("12345123451234512345"))

    panel2 = RadioPanel(lambda: stop, verbose, actionMapping1, usbBus=0, usbAddress=3)
    panel2.connect()
    panel2.print_message(lcd.convert_string_to_bytes("1.2 4.5-12.34  123 123"))

    print('Press Ctrl+C to exit')
    while not stop:
        time.sleep(0.1)
        if threading.active_count() <= 1:
            print("All devices disconnected.")
            stop = True


if __name__ == "__main__":
    main()
