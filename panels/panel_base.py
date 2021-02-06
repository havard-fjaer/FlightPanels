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

    def device_name(self, device):
        return "USB:"\
            + hex(device.idVendor) + ":" \
            + hex(device.idProduct) + ":" \
            + str(device.bus) + ":" \
            + str(device.address)

    def run(self):
        devices = usb.core.find(idVendor=self.idVendor,
                                idProduct=self.idProduct, 
                                find_all=True)
        for device in devices:
            if device is not None:
                name = self.device_name(device)
                thread = threading.Thread(target=self.monitor_device, args=(device, name))
                print(name + " connected")
                thread.name = name
                thread.start()

    def monitor_device(self, dev, name):
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
        while not self.stop():
            try:
                # Endpoint: 0x81, Buffer: 3 bytes
                data = dev.read(0x81, 3)
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
                    print(name + " - " + str(e.backend_error_code))
