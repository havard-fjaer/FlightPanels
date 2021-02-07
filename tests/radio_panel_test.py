import unittest
import panels.radio_panel

class TestStringMethods(unittest.TestCase):
  
    def test_show_state_change(self):
        radio = panels.radio_panel.RadioPanel(False, True, None)

        intital_state_bytes = b'\x00\x00\x10'
        radio.update_state(intital_state_bytes)
        initial_state = radio.bit_state
        
        new_state_bytes = b'\x00\x00\x01'
        state_change = radio.compare_to_previous_state(new_state_bytes)
        new_state = int.from_bytes(new_state_bytes, "big")

        print("Initial state: " + format(initial_state, '024b'))
        print("New state:     " + format(new_state, '024b'))
        print("State change:  " + format(state_change, '024b'))
        self.assertEqual(0b00001, state_change)