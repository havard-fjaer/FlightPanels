from panels.radio_panel import RadioPanel
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
    panel1.connect()
    panel1.print_message("Test")

    panel2 = RadioPanel(lambda: stop, verbose, usbBus=0, usbAddress=3)
    panel2.connect()

    print('Press Ctrl+C to exit')
    while not stop:
        time.sleep(0.1)
        if threading.active_count() <= 1:
            print("All devices disconnected.")
            stop = True


if __name__ == "__main__":
    main()
