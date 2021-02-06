import usb.util as util
from panels.radio_panel_flag import RadioPanelButtonFlag
from panels.panel_base import PanelBase


class RadioPanel(PanelBase):
    def __init__(self, stop, verbose, actionMapping, usbBus=None, usbAddress=None):
        super().__init__(stop, verbose, 0x06a3, 0x0d05, usbBus, usbAddress)
        self.button_state = 0
        self.actionMapping = actionMapping

    def print_message(self, message):
        if not self.device_is_ready:
            print("Device is not ready yet.")
            return
        # Send control message
        #           0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        data = b'\xd4\x01\x0f\xd3\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04\x00\x01\x02\x03\x04'
        outType = util.build_request_type(
            util.CTRL_OUT, util.CTRL_TYPE_CLASS, util.CTRL_RECIPIENT_INTERFACE)  # 0x21
        self.device.ctrl_transfer(outType, 0x09, 0x03, 0x00, data)

    def read_from_device(self):
        # Endpoint: 0x81, Buffer: 3 bytes
        data = self.device.read(0x81, 3)
        changed_buttons = self.update_button_state(data)
        for cb in changed_buttons:
            if cb in self.actionMapping.keys():
                self.actionMapping[cb]()
            if self.verbose:
                print(self.device_name() + ":" + cb.name)

    def update_button_state(self, state):

        changed_state = self.compare_to_button_state(state)
        changed_to_active = list()
        for bf in RadioPanelButtonFlag:
            if changed_state & bf.value != 0:
                changed_to_active.append(bf)
        self.button_state = int.from_bytes(state, "big")
        return changed_to_active

    def compare_to_button_state(self, state):
        new_state = int.from_bytes(state, "big")
        old_state = self.button_state

        changed_state = (
            new_state ^ old_state  # XOR for checking change
            & new_state  # and AND to return only active bits
        )
        return changed_state
