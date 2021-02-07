import time
from panels.radio_panel_flag import *
from modules.stopwatch import RadioPanelStopWatch
class RadioPanelDemoService:
    def __init__(self) -> None:
        self.panel = None
        self.stop = False
        self.stopwatch = RadioPanelStopWatch()


    def close(self):
        print("Closing Radio Panel Demo Service.")
        self.stopwatch.close()
        self.stop = True

    def connect_panel(self, panel):
        self.panel = panel
        self.panel.map_actions({
            RadioPanelFlag.ACT_STDBY_1: self.toggle_stop_watch,
            RadioPanelFlag.ENCODER_INNER_CCW_1: lambda: print("Inner CCW 1 - dev1"),
        })

    def toggle_stop_watch(self):
        self.stopwatch.display = self.panel.set_lcd1
        self.stopwatch.toggle_stop_watch()

    def run(self):
        while not self.stop:
            time.sleep(0.1)
            # now = datetime.now()
            # current_time = now.strftime(" %M.%S")
            # self.panel.set_lcd(RadioPanelLcd.LCD1, current_time)
            # self.panel.set_lcd(RadioPanelLcd.LCD2, current_time)
            # self.panel.set_lcd(RadioPanelLcd.LCD3, current_time)
            # self.panel.set_lcd(RadioPanelLcd.LCD4, current_time)

