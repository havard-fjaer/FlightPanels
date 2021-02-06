import threading
import time
import usb.core


class PanelBase(object):
    def __init__(self, stop, verbose, idVendor, idProduct, usbBus=None, usbAddress=None):
        self.stop = stop
        self.verbose = verbose
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.usbBus = usbBus
        self.usbAddress = usbAddress
        self.device = None
        self.device_is_ready = False
        self.connect()

    def connect(self):
        devices = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct, find_all=True)
        for device in devices:
            if device is not None:
                if self.usbBus == device.bus and self.usbAddress == device.address:
                    self.connect_device(
                        device, "Connecting to specified USB device: " + self.device_name(device))
                    return
                elif self.usbBus == None or self.usbAddress == None:
                    self.connect_device(
                        device, "Connecting to first available USB device: " + self.device_name(device))
                    return
                else:
                    print(self.device_name(device) + " skipped.")

    def connect_device(self, device, message):
        print(message)
        device.set_configuration()
        self.device = device
        thread = threading.Thread(target=self.monitor_device)
        thread.start()
        self.device_is_ready = True
        print(self.device_name() + " connected. Starting monitoring.")

    def monitor_device(self):
        # Read from endpoint
        while not self.stop():
            try:
                self.read_from_device()  # Hook must be implemented in inheriting class!
                time.sleep(0.01)
            except usb.core.USBError as e:
                if e.backend_error_code == -116:
                    pass  # Ignore timeouts when reading empty data
                elif e.backend_error_code == -5:
                    print(self.device_name() + " disconnected.")
                    break
                else:
                    print(
                        self.device_name() + " - USB backend error code: " + str(e.backend_error_code))

    def device_name(self, device=None):
        if device is not None:
            dev = device
        else:
            dev = self.device
        return "USB:"\
            + hex(dev.idVendor) + ":" \
            + hex(dev.idProduct) + ":" \
            + str(dev.bus) + ":" \
            + str(dev.address)
