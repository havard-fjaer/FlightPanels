import threading
class NumberModule:

    BLANK_ERROR = "     "
    DASH_ERROR = "-----"

    def __init__(self, number, max_string_len=5, error_blink_interval=0.5):
        self.number = number
        self.max_string_len = max_string_len
        self.timer = None
        self.is_closing = False
        self.error_message = self.DASH_ERROR
        self.error_blink_interval = error_blink_interval
    
    def close(self):
        if self.timer is not None:
            self.timer.cancel()
        self.is_closing = True

    def set(self, number):
        self.number = number
        self.update_display()

    def inc(self, inc):
        self.number += inc
        self.update_display()
       
    def update_display(self):
        if self.string_is_too_long():
            if self.timer is None:
                self.blink_error()
            return
        
        if self.lcd_handler is not None:
            self.lcd_handler(self.number_as_string())           


    def blink_error(self):

        if self.string_is_too_long() and not self.is_closing:
            self.timer = threading.Timer(self.error_blink_interval, self.blink_error)
            self.timer.start()
        elif self.timer is not None:
                self.timer.cancel()
                self.timer = None            

        if self.string_is_too_long() and self.lcd_handler is not None:
            if self.error_message is self.DASH_ERROR:
                self.error_message = self.number_error_message()            
            else:
                self.error_message = self.DASH_ERROR
            self.lcd_handler(self.error_message)

    def number_error_message(self):
        if self.number > 0:
            return "9"*(self.max_string_len)
        else:
            return "-" + "9"*(self.max_string_len-1)

    def string_is_too_long(self):
        return len(self.number_as_string()) > self.max_string_len

    def number_as_string(self):
        return str(self.number).rjust(self.max_string_len, ' ')

