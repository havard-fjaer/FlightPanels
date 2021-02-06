def convert_string_to_bytes(str):
    bytes = bytearray()

    for i in range(len(str)):
        ascii = ord(str[i])

        # Check if next character is a . dot
        dot = 0xd0 if next_char_is_dot(str, i) else 0x00

        # Is a digit
        if ascii >= 0x30 and ascii <= 0x39:
            # Digits 0 to 9 = x : 0000xxxx
            bytes.append(ascii - 0x30 + dot)

        # Is a "-" hyphen
        if ascii == 0x2d:
            bytes.append(0xe0)  # Hyphen = 1110xxxx

        # Is a " " space
        if ascii == 0x20:
            bytes.append(0x0f)  # Empty = 00001111

    return bytes

def next_char_is_dot(str, i):
    return (
        i + 1 < len(str) # There are more characters in string
        and
        ord(str[i + 1]) == 0x2e # Next character is a dot .
    )

def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]
