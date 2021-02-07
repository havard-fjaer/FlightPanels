import threading
import time
class RadioPanelStopWatch:
    def __init__(self) -> None:
        self.is_running = False
        self.is_reset = True
        self.tart_time = time.time()   
        self.display = None 
        self.timer = None

    def close(self):
        if self.timer is not None:
            print("Closing Stopwatch")
            self.timer.cancel()

    def toggle_stop_watch(self):

        if self.is_running:
            self.close()
            self.is_running = False

        elif not self.is_running and not self.is_reset:
            self.display(time_convert(0))
            self.is_reset = True

        elif not self.is_running and self.is_reset:
            self.is_running = True
            self.is_reset = False
            self.stop_watch_start_time = time.time()
            self.update_stop_watch()        


    def update_stop_watch(self):
        time_diff = time.time() - self.stop_watch_start_time
        self.display(time_convert(time_diff))

        self.timer = threading.Timer(1.0, self.update_stop_watch)
        self.timer.start()



def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    mins = mins % 60
    return f' {int(mins):02d}.{int(sec):02d}'
