import time
from panels.radio_panel_flag import *
class RadioPanelDemoService:
    def __init__(self) -> None:
        self.panel = None
        self.stop = False

    def close(self):
        print("Closing Radio Panel Demo Service.")
        self.stop = True

    def connect_panel(self, panel):
        self.panel = panel
        self.panel.map_actions({
            RadioPanelFlag.ENCODER_INNER_CW_1: lambda: print("Inner CW 1 - dev1"),
            RadioPanelFlag.ENCODER_INNER_CCW_1: lambda: print("Inner CCW 1 - dev1"),
            RadioPanelFlag.ENCODER_INNER_CW_2: lambda: self.panel.set_lcd(RadioPanelLcd.LCD1, "11111111111111111111"),
            RadioPanelFlag.ENCODER_INNER_CCW_2: lambda: self.panel.set_lcd(RadioPanelLcd.LCD1, "22222222222222222222"),
        })

    def run(self):
        while not self.stop:
            print("In RadioPanelDemoService")
            time.sleep(5)
