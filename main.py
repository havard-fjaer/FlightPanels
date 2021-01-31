#!/usr/bin/python
import usb.core
import usb.util as util

dev = usb.core.find(idVendor=0x06a3, idProduct=0x0d05)
if dev is None:
    raise ValueError('Radio Panel PZ69 not found')
dev.set_configuration()


#           0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19 
data = b'\xd2\x01\x0f\xd3\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04'

bmRequestType = util.build_request_type(util.CTRL_OUT, util.CTRL_TYPE_CLASS, util.CTRL_RECIPIENT_INTERFACE) #0x21
dev.ctrl_transfer(bmRequestType, 0x09, 0x03, 0x00, b'\xd1\x01\x0f\xd3\x04\xe0\x01\x02\xd3\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04')
