import usb.util as util
from panels.panel_text_converter import *
from panels.radio_panel_flag import *
from panels.panel_base import *
class RadioPanel(PanelBase):

    USB_VENDOR = 0x06a3 # Logitech
    USB_PRODUCT = 0x0d05 # Radio Panel

    def __init__(self, usb_bus=None, usb_address=None, verbose=False):

        super().__init__(RadioPanel.USB_VENDOR, RadioPanel.USB_PRODUCT, usb_bus, usb_address, verbose)
        self.button_state = 0
        self.action_mapping = None

    def map_actions(self, action_mapping):
        self.action_mapping = action_mapping

    def set_lcd(self, lcd, str):
        lcd.value # TODO
        self.display_state = str
        self.update_displays()


    def update_displays(self):
        text_bytes = convert_string_to_bytes(self.display_state)
        outType = util.build_request_type(util.CTRL_OUT, util.CTRL_TYPE_CLASS, util.CTRL_RECIPIENT_INTERFACE)  # 0x21
        self.device.ctrl_transfer(outType, 0x09, 0x03, 0x00, text_bytes)

    def read_from_device(self):
        # Endpoint: 0x81, Buffer: 3 bytes
        data = self.device.read(0x81, 3)
        changed_buttons = self.update_button_state(data)
        for cb in changed_buttons:
            if self.action_mapping != None and cb in self.action_mapping.keys():
                self.action_mapping[cb]()
            if self.verbose:
                print(self.device_name() + ":" + cb.name)

    def update_button_state(self, state):
        changed_state = self.compare_to_button_state(state)
        changed_to_active = list()
        for bf in RadioPanelFlag:
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
