import usb.util as util
from panels.panel_text_converter import *
from panels.radio_panel_flag import *
from panels.panel_base import *


class RadioPanel(PanelBase):
    """
    Logic specific to Radio Panel:
    - Implementing reading and converting button states, 
    - Passing and converting strings to bytes, updating the LED displays.
    """
    USB_VENDOR = 0x06a3  # Logitech
    USB_PRODUCT = 0x0d05  # Radio Panel

    LCD_BLANK = "     "
    LCD_DASHES = "-----"

    def __init__(self, service=None, usb_bus=None, usb_address=None, verbose=False):
        super().__init__(RadioPanel.USB_VENDOR,
                         RadioPanel.USB_PRODUCT, usb_bus, usb_address, verbose)
        self.event_handlers = None # Exposes all bit changes
        self.state_handler = None  # Exposes radio states when changed
        self.bit_state = 0
        self.radio1_state = None
        self.radio2_state = None
        self.lcd_state = {
            RadioPanelLcd.LCD1: RadioPanel.LCD_DASHES,
            RadioPanelLcd.LCD2: RadioPanel.LCD_DASHES,
            RadioPanelLcd.LCD3: RadioPanel.LCD_DASHES,
            RadioPanelLcd.LCD4: RadioPanel.LCD_DASHES,
        }
        # Connect service only after panel is initialized
        if service is not None:
            self.service = service
            self.service.connect_panel(self)

    def close(self):
        PanelBase.close(self)
        self.service.close()

    def set_event_handlers(self, event_handlers):
        self.event_handlers = event_handlers()

    def set_state_handler(self, state_handler): 
        self.state_handler = state_handler

    def set_lcd(self, lcd, str):
        self.lcd_state[lcd] = str
        self.update_displays()

    def set_lcd1(self, str):
        self.set_lcd(RadioPanelLcd.LCD1, str)

    def set_lcd2(self, str):
        self.set_lcd(RadioPanelLcd.LCD2, str)

    def set_lcd3(self, str):
        self.set_lcd(RadioPanelLcd.LCD3, str)

    def set_lcd4(self, str):
        self.set_lcd(RadioPanelLcd.LCD4, str)

    def clear_lcd(self):
        self.lcd_state[RadioPanelLcd.LCD1] = RadioPanel.LCD_BLANK
        self.lcd_state[RadioPanelLcd.LCD2] = RadioPanel.LCD_BLANK
        self.lcd_state[RadioPanelLcd.LCD3] = RadioPanel.LCD_BLANK
        self.lcd_state[RadioPanelLcd.LCD4] = RadioPanel.LCD_BLANK
        self.update_displays()        

    def update_displays(self):
        """
        Converts strings to radio panel bytes, and updates the displays.
        """
        display_state = ""
        for value in self.lcd_state.values():
            display_state += value
        text_bytes = convert_string_to_bytes(display_state)
        outType = util.build_request_type(
            util.CTRL_OUT, util.CTRL_TYPE_CLASS, util.CTRL_RECIPIENT_INTERFACE)  # 0x21
        self.device.ctrl_transfer(outType, 0x09, 0x03, 0x00, text_bytes)

    def read_from_device(self):
        """
        Reads from the device, and triggers any mapped 
        actions corresponding to buttons that have changed.
        """
        # Endpoint: 0x81, Buffer: 3 bytes
        new_byte_state = self.device.read(0x81, 3)
        new_bit_state = convert_bytes_to_int(new_byte_state)
        changed_states = self.calculate_changed_state(new_bit_state)
        self.trigger_event_handlers(changed_states)
        self.trigger_state_handler(new_bit_state)
        self.update_bit_state(new_bit_state)

    def calculate_changed_state(self, new_bit_state):
        """
        Identifies changed bits, and returns the newly active ones.
        """
        changed_state = (
            new_bit_state ^ self.bit_state  # XOR for checking change
            & new_bit_state  # and AND to return only active bits
        )
        return changed_state

    def trigger_event_handlers(self, changed_state):
        event_flags = convert_bits_to_flags(changed_state)
        for cb in event_flags:
            if self.event_handlers != None and cb in self.event_handlers.keys():
                self.event_handlers[cb]()
            if self.verbose:
                print(self.device_name() + ":" + cb.name)

    def trigger_state_handler(self, new_bit_state):
        if self.state_handler is None:
            return

        new_radio1_state = None
        new_radio2_state = None
        new_button_state = convert_bits_to_flags(new_bit_state)
        for button in new_button_state:
            if RadioPanelFlag.is_radio1_state(button):
                new_radio1_state = button
            if RadioPanelFlag.is_radio2_state(button):
                new_radio2_state = button

        # Trigger handler if any radio has changed state
        radio1_changed = new_radio1_state is not self.radio1_state
        radio2_changed = new_radio2_state is not self.radio2_state
        if (radio1_changed or radio2_changed):
            self.radio1_state = new_radio1_state
            self.radio2_state = new_radio2_state
            self.state_handler(new_radio1_state, new_radio2_state)

    def update_bit_state(self, new_bit_state):
        self.bit_state = new_bit_state

def convert_bits_to_flags(bits):
    buttons = list()
    for bf in RadioPanelFlag:
        if bits & bf.value != 0:
            buttons.append(bf)
    return buttons

def convert_bytes_to_int(bytes):
    return int.from_bytes(bytes, "big")
