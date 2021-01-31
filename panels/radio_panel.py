from panels.radio_panel_flag import RadioPanelButtonFlag
class RadioPanel():
    def __init__(self):
        self.button_state = 0

    def update_button_state(self, state):

        changed_state = self.compare_to_button_state(state)
        changed_to_active = list()
        for bf in RadioPanelButtonFlag:
            if changed_state & bf.value != 0:
                changed_to_active.append(bf)
        self.button_state = int.from_bytes(state, "big")
        return changed_to_active
    
    def compare_to_button_state(self, state):
        new_state = int.from_bytes(state, "big")
        old_state = self.button_state

        changed_state = (
            new_state ^ old_state # XOR for checking change
            & new_state # and AND to return only active bits
        )
        return changed_state

