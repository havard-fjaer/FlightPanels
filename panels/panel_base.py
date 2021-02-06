import threading
import time
import usb.core
import usb.util as util
from panels.radio_panel import RadioPanel


class PanelBase(object):
    def __init__(self, stop, verbose, idVendor, idProduct, usbBus=None, usbAddress=None):
        self.stop = stop
        self.verbose = verbose
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.usbBus = usbBus
        self.usbAddress = usbAddress
        self.device_is_ready = False


    def run(self):
        devices = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct, find_all=True)
        for device in devices:
            if device is not None:
                if self.usbBus == device.bus and self.usbAddress == device.address:
                    self.connect_device(device, "Connecting to specified USB device.")
                elif self.usbBus == None or self.usbAddress == None:
                    self.connect_device(device, "Connecting to first available USB device.")
                else:
                    print(self.device_name(device) + " skipped.")


    def device_name(self, device):
        return "USB:"\
            + hex(device.idVendor) + ":" \
            + hex(device.idProduct) + ":" \
            + str(device.bus) + ":" \
            + str(device.address)

    def connect_device(self, device, message):
        print(message)
        name = self.device_name(device)
        device.set_configuration()
        self.device = device
        self.device_is_ready = True
        thread = threading.Thread(target=self.monitor_device)
        print(name + " connected. Starting monitoring for events.")
        thread.start()

    def print_message(self, message):
        if not self.device_is_ready:
            print("Device is not ready yet.")
            return
        # Send control message
        #           0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        data = b'\xd4\x01\x0f\xd3\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04'
        outType = util.build_request_type(util.CTRL_OUT, util.CTRL_TYPE_CLASS, util.CTRL_RECIPIENT_INTERFACE)  # 0x21
        self.device.ctrl_transfer(outType, 0x09, 0x03, 0x00, data)

    def monitor_device(self):
        name = self.device_name(self.device)

        # Read from endpoint
        radio_panel = RadioPanel()
        while not self.stop():
            try:
                # Endpoint: 0x81, Buffer: 3 bytes
                data = self.device.read(0x81, 3)
                changed_buttons = radio_panel.update_button_state(data)
                if self.verbose:
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
                    print(name + " - USB backend error code: " + str(e.backend_error_code))
