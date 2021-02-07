import threading
import time
class RadioPanelStopWatch:
    def __init__(self, should_restart_immediatly=False, should_reset_to_zero=False):
        self.is_running = False
        self.is_reset = False
        self.stop_watch_start_time = None
        self.should_reset_to_zero = should_reset_to_zero
        self.should_restart_immediatly = should_restart_immediatly
        self.start_time = time.time()  
        self.time_diff = 0 
        self.is_closing = False
        self.display = None 
        self.timer = None

    def close(self):
        if self.timer is not None:
            print("Closing Stopwatch")
            self.is_closing = True
            self.timer.cancel()

    def toggle_stop_watch(self):

        if self.is_closing:
            return

        if self.is_running and not self.should_restart_immediatly:
            self.timer.cancel()
            self.is_running = False

        elif not self.is_reset and self.should_reset_to_zero:
            self.display(time_convert(0))
            self.is_reset = True

        else:
            self.is_running = True
            self.is_reset = False
            self.stop_watch_start_time = time.time()
            if self.timer is not None:
                self.timer.cancel()
            self.update_stop_watch()        


    def update_stop_watch(self):
        if self.stop_watch_start_time is None:
            self.time_diff = 0
        else:
            self.time_diff = time.time() - self.stop_watch_start_time
        if self.lcd_handler is not None:
            self.lcd_handler(time_convert(self.time_diff))

        self.timer = threading.Timer(1.0, self.update_stop_watch)
        self.timer.start()



def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return f'{int(hours):01d}.{int(mins):02d}.{int(sec):02d}'
