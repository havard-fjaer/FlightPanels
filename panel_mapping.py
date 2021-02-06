"""
Demo mapping of actions to panel events. Implement something similar in your own application.
"""
import sys
from panels.radio_panel import RadioPanel
from panels.radio_panel_flag import *

def is_verbose():
    args = sys.argv[1:]
    return '-v' in args

def create_radio_panel_1():
    panel1 = RadioPanel(usb_bus=0, usb_address=1, verbose=is_verbose())
    if panel1.device_is_ready:
        panel1.map_actions({
            RadioPanelFlag.ENCODER_INNER_CW_1: lambda: print("Inner CW 1 - dev1"),
            RadioPanelFlag.ENCODER_INNER_CCW_1: lambda: print("Inner CCW 1 - dev1"),
        })
        panel1.set_lcd(RadioPanelLcd.LCD1, "12345678900987654321")
    else:
        print("Failed to load device.")
    return panel1

def create_radio_panel_2():
    panel2 = RadioPanel(usb_bus=0, usb_address=2, verbose=is_verbose())
    if panel2.device_is_ready:
        panel2.map_actions({
            RadioPanelFlag.ENCODER_INNER_CW_1: lambda: panel2.set_lcd(RadioPanelLcd.LCD1, "11111111111111111111"),
            RadioPanelFlag.ENCODER_INNER_CCW_1: lambda: panel2.set_lcd(RadioPanelLcd.LCD1, "22222222222222222222"),
        })
        panel2.set_lcd(RadioPanelLcd.LCD1, "12345678900987654321")
    else:
        print("Failed to load device.")
    return panel2
