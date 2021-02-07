import time
from panels.radio_panel_flag import *
from modules.stopwatch import RadioPanelStopWatch
class RadioPanelDemoService:
    def __init__(self) -> None:
        self.panel = None
        self.is_closing = False
        self.stopwatch = RadioPanelStopWatch(should_restart_immediatly=True)
        self.stopwatch2 = RadioPanelStopWatch(should_restart_immediatly=True)


    def close(self):
        print("Closing Radio Panel Demo Service.")
        self.stopwatch.close()
        self.stopwatch2.close()
        self.is_closing = True

    def connect_panel(self, panel):
        self.panel = panel
        self.panel.clear_lcd()
        self.panel.set_event_handlers(self.event_handlers)
        self.panel.set_radio_state_handler(self.radio_state_handler)

    def event_handlers(self):
        return {
            RadioPanelFlag.ENCODER_INNER_CCW_1: lambda: print("Inner CCW 1 - dev1"),
            RadioPanelFlag.ENCODER_INNER_CW_1: lambda: print("Inner CW 1 - dev1"),
        }

    def radio_state_handler(self, radio1_state, radio2_state):
        print("Radio 1: " + radio1_state.name)
        print("Radio 2: " + radio2_state.name)

        if radio1_state is RadioPanelFlag.XPDR_1: # Init
            self.stopwatch.lcd_handler = self.panel.set_lcd1
            self.stopwatch.update_stop_watch()
            self.panel.event_handlers[RadioPanelFlag.ACT_STDBY_1] = self.stopwatch.toggle_stop_watch
        if radio1_state is not RadioPanelFlag.XPDR_1: # Cleanup
            self.stopwatch.lcd_handler = None

        if radio1_state is RadioPanelFlag.DME_1:
            self.stopwatch2.lcd_handler = self.panel.set_lcd1
            self.stopwatch2.update_stop_watch()
            self.panel.event_handlers[RadioPanelFlag.ACT_STDBY_1] = self.stopwatch2.toggle_stop_watch
        if radio1_state is not RadioPanelFlag.DME_1:
            self.stopwatch2.lcd_handler = None


    def run(self):
        while not self.is_closing:
            time.sleep(0.1)

