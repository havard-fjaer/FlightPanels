import signal
import sys
import threading
import time
import usb.core
import usb.util as util
from panels.radio_panel import RadioPanel


def monitor_device(dev, name, verbose, stop):
    if dev is None:
        raise ValueError('Radio Panel PZ69 not found')
    dev.set_configuration()

    # Send control message
    #           0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
    data = b'\xd4\x01\x0f\xd3\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04'
    outType = util.build_request_type(
        util.CTRL_OUT, util.CTRL_TYPE_CLASS, util.CTRL_RECIPIENT_INTERFACE)  # 0x21
    dev.ctrl_transfer(outType, 0x09, 0x03, 0x00, data)

    # Read from endpoint
    radio_panel = RadioPanel()
    while not stop():
        try:
            # Endpoint: 0x81, Buffer: 3 bytes
            data = dev.read(0x81, 3)
            changed_buttons = radio_panel.update_button_state(data)
            if verbose:
                for cb in changed_buttons:
                    print(name + ":" + cb.name)
            time.sleep(0.01)
        except usb.core.USBError as e:
            if e.backend_error_code == -116:
                pass  # Ignore timeouts when reading empty data
            elif e.backend_error_code == -5:
                print(name + " disconnected.")
                break
            else:
                print(name + " - " + str(e.backend_error_code))


def signal_handler(sig, frame):
    print("Signal '{0}' received. Stopping threads.".format(
        signal.Signals(sig).name))
    global stop
    stop = True


def main():
    global stop
    args = sys.argv[1:]
    if '-v' in args:
        verbose = True
    else:
        verbose = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    devices = usb.core.find(idVendor=0x06a3, idProduct=0x0d05, find_all=True)
    threads = list()
    stop = False
    for dev in devices:
        if dev is not None:
            name = "USB:" + hex(dev.idVendor) + ":" + hex(dev.idProduct) + \
                ":" + str(dev.bus) + ":" + str(dev.address)
            thread = threading.Thread(target=monitor_device, args=(
                dev, name, verbose, lambda: stop))
            print(name + " connected")
            thread.name = name
            threads.append(thread)
            thread.start()

    print('Press Ctrl+C to exit')
    while not stop:
        time.sleep(1)  # Wait for SIG*
        if threading.active_count() <= 1:
            print("All devices disconnected.")
            stop = True


if __name__ == "__main__":
    main()
