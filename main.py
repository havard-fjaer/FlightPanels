import time
import usb.core
import usb.util as util
import threading
import keyboard


def monitor_device(dev, name, stop):
    if dev is None:
        raise ValueError('Radio Panel PZ69 not found')
    dev.set_configuration()
    # print(dev)

    # Send control message
    #           0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19 
    data = b'\xd4\x01\x0f\xd3\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04'
    outType = util.build_request_type(util.CTRL_OUT, util.CTRL_TYPE_CLASS, util.CTRL_RECIPIENT_INTERFACE) #0x21
    dev.ctrl_transfer(outType, 0x09, 0x03, 0x00, data)

    # Read from endpoint
    while not stop():     
        try:
            # Endpoint: 0x81, Buffer: 3 bytes
            data = dev.read(0x81, 3)
            print(name + " - " + str(data))
            time.sleep(0.01)
        except KeyboardInterrupt:
            break
        except usb.core.USBError as e:
            if e.backend_error_code == -116:
                pass # Ignore timeouts when reading empty data
            else:
                print(name + " - " + e.args)

def print_threads(dummy):
    print("Running threads:")
    for t in threads:
        print(t.name)

def stop_threads(dummy):
    print("Stopping threads")
    global stop 
    stop = True 

keyboard.on_release_key('t', print_threads)
keyboard.on_release_key(57, stop_threads)

devices = usb.core.find(idVendor=0x06a3, idProduct=0x0d05, find_all=True)
threads = list()
stop = False
for dev in devices:
    if dev is not None:
        name = "USB:" + hex(dev.idVendor) + ":" + hex(dev.idProduct) + ":" + str(dev.bus) + ":" +  str(dev.address)
        thread = threading.Thread(target=monitor_device, args=(dev,name,lambda : stop))
        print(name)
        thread.name = name
        threads.append(thread)
        thread.start()