import time
import usb.core


class PanelBase(object):
    """
    Finds and connects to specified USB devices. 
    Usage: Inherit class, and implement self.read_from_device() to react to USB events.
    Note: Updating displays must be implemented in the inheriting class, using calls to self.device.ctrl_transfer()
    """    
    def __init__(self, id_vendor, id_product, usb_bus=None, usb_address=None, verbose=False):
        self.stop = False
        self.verbose = verbose
        self.id_vendor = id_vendor
        self.id_product = id_product
        self.usb_bus = usb_bus
        self.usb_address = usb_address
        self.device = None
        self.device_is_ready = False
        self.connect()

    def close(self):
        self.stop = True  

    def connect(self):
        """
        Finds and connects to a specified device, or the first device for a given vendor and product.
        """
        devices = usb.core.find(idVendor=self.id_vendor, idProduct=self.id_product, find_all=True)
        for device in devices:
            if device is not None:
                if self.usb_bus == device.bus and self.usb_address == device.address:
                    self.connect_device(
                        device, "Connecting to specified USB device: " + self.device_name(device))
                    return
                elif self.usb_bus == None or self.usb_address == None:
                    self.connect_device(
                        device, "Connecting to first available USB device: " + self.device_name(device))
                    return
                else:
                    print(self.device_name(device) + " skipped.")

    def connect_device(self, device, message):
        """
        Connects, starts and spins up a thread for listening to the device.
        """
        print(message)
        device.set_configuration()
        self.device = device
        if self.verbose:
            print(device)        
        self.device_is_ready = True
        print(self.device_name() + " connected. Starting monitoring.")


    def monitor_device(self):
        """
        Loops over the device, calling self.read_from_device() to read any new data using self.device.read().
        """        
        # Read from endpoint
        while not self.stop:
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
