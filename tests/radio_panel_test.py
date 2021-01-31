import unittest
import panels.radio_panel

class TestStringMethods(unittest.TestCase):

    def test_com1_button(self):
        radio = panels.radio_panel.RadioPanel()
        
        radio.set_button_state(b'\x00\x00\x00')
        state = radio.get_com1_state()
        print("State: " + str(state))
        self.assertFalse(state)  

        radio.set_button_state(b'\x00\x00\x01')
        state = radio.get_com1_state()
        print("State: " + str(state))
        self.assertTrue(state)


