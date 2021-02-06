import unittest
import panels.panel_text_converter


class PanelTextConverterTest(unittest.TestCase):

    def test_various_combination(self):
        lcd = panels.panel_text_converter.PanelTextConverter()
        result = lcd.convert_string_to_bytes("!0.123-56 78.9.xyz")
        self.assertEqual(result, b'\xd0\x01\x02\x03\xe0\x05\x06\x0f\x07\xd8\xd9')

    def test_string_of_digits(self):
        lcd = panels.panel_text_converter.PanelTextConverter()
        result = lcd.convert_string_to_bytes("0123456789")
        self.assertEqual(result, b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09')

    def test_string_with_hyphen(self):
        lcd = panels.panel_text_converter.PanelTextConverter()
        result = lcd.convert_string_to_bytes("-")
        self.assertEqual(result, b'\xe0')  # Hyphen = 1110xxxx

    def test_string_with_space(self):
        lcd = panels.panel_text_converter.PanelTextConverter()
        result = lcd.convert_string_to_bytes(" ")
        self.assertEqual(result, b'\x0f')  # Empty = 00001111

    def test_string_with_dots(self):
        lcd = panels.panel_text_converter.PanelTextConverter()
        result = lcd.convert_string_to_bytes("0.0")
        self.assertEqual(result, b'\xd0\x00')

    def test_ignore_double_dots(self):
        lcd = panels.panel_text_converter.PanelTextConverter()
        result = lcd.convert_string_to_bytes("0..0")
        self.assertEqual(result, b'\xd0\x00')

    def test_ignore_preceeding_dots(self):
        lcd = panels.panel_text_converter.PanelTextConverter()
        result = lcd.convert_string_to_bytes(".0")
        self.assertEqual(result, b'\x00')

    def test_exclude_unknown_characters(self):
        lcd = panels.panel_text_converter.PanelTextConverter()
        result = lcd.convert_string_to_bytes("abcdefXYZ,_!#¤%&/()=")
        self.assertEqual(result, b'')
