from enum import IntEnum, IntFlag
class RadioPanelFlag(IntFlag):
    COM1_1 = 1 << 16
    COM2_1 = 2 << 16
    NAV1_1 = 4 << 16
    NAV2_1 = 8 << 16
    ADF_1 = 16 << 16
    DME_1 = 32 << 16
    XPDR_1 = 64 << 16
    COM1_2 = 128 << 16
    COM2_2 = 1 << 8
    NAV1_2 = 2 << 8
    NAV2_2 = 4 << 8
    ADF_2 = 8 << 8
    DME_2 = 16 << 8
    XPDR_2 = 32 << 8
    ACT_STDBY_1 = 64 << 8
    ACT_STDBY_2  = 128 << 8
    ENCODER_INNER_CW_1 = 1
    ENCODER_INNER_CCW_1 = 2
    ENCODER_OUTER_CW_1 = 4
    ENCODER_OUTER_CCW_1 = 8    
    ENCODER_INNER_CW_2 = 16
    ENCODER_INNER_CCW_2 = 32
    ENCODER_OUTER_CW_2 = 64
    ENCODER_OUTER_CCW_2 = 128

class RadioPanelLcd(IntEnum):
    # Byte offsets per LCD
    LCD1 = 0
    LCD2 = 5
    LCD3 = 10
    LCD4 = 15