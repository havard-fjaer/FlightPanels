class RadioPanel():

    def __init__(self):
        self.button_state = bytes(3)

    def set_button_state(self, state):
        self.button_state = state

    def get_com1_state(self):
        return self.button_state[2] & 1