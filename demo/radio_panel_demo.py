from modules.number import NumberModule
import time
from panels.radio_panel_flag import *
from modules.stopwatch import RadioPanelStopWatch
class RadioPanelDemoService:
    def __init__(self) -> None:
        self.panel = None
        self.is_closing = False
        self.stopwatch1 = RadioPanelStopWatch(should_restart_immediatly=True)
        self.stopwatch2 = RadioPanelStopWatch(should_restart_immediatly=True)
        self.number1 = NumberModule(0)


    def close(self):
        print("Closing Radio Panel Demo Service.")
        self.stopwatch1.close()
        self.stopwatch2.close()
        self.number1.close()
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

        if radio1_state is RadioPanelFlag.ADF_1: 
            self.panel.event_handlers[RadioPanelFlag.ACT_STDBY_1] = lambda: self.number1.set(0)
            self.panel.event_handlers[RadioPanelFlag.ENCODER_INNER_CW_1]  = lambda: self.number1.inc(1)
            self.panel.event_handlers[RadioPanelFlag.ENCODER_INNER_CCW_1] = lambda: self.number1.inc(-1)            
            self.panel.event_handlers[RadioPanelFlag.ENCODER_OUTER_CW_1]  = lambda: self.number1.inc(1000)
            self.panel.event_handlers[RadioPanelFlag.ENCODER_OUTER_CCW_1] = lambda: self.number1.inc(-1000)
            self.number1.lcd_handler = self.panel.set_lcd1
            self.number1.update_display()
        
        if radio1_state is RadioPanelFlag.DME_1: # Init
            self.stopwatch2.lcd_handler = self.panel.set_lcd1
            self.stopwatch2.update_stop_watch()
            self.panel.event_handlers[RadioPanelFlag.ACT_STDBY_1] = self.stopwatch2.toggle_stop_watch
        if radio1_state is not RadioPanelFlag.DME_1: # Cleanup -  only for service resources. Panel settings should be reset in the other state mappers.
            self.stopwatch2.lcd_handler = None
        
        if radio1_state is RadioPanelFlag.XPDR_1:
            self.stopwatch1.lcd_handler = self.panel.set_lcd1
            self.stopwatch1.update_stop_watch()
            self.panel.event_handlers[RadioPanelFlag.ACT_STDBY_1] = self.stopwatch1.toggle_stop_watch
        if radio1_state is not RadioPanelFlag.XPDR_1:
            self.stopwatch1.lcd_handler = None




    def run(self):
        while not self.is_closing:
            time.sleep(0.1)

