from enum import IntEnum, IntFlag


class RadioPanelFlag(IntFlag):

    def is_radio1_flag(state):
        return is_radiox_state(state, radio1_states())

    def is_radio2_flag(state):
        return is_radiox_state(state, radio2_states())

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
    ACT_STDBY_2 = 128 << 8
    ENCODER_INNER_CW_1 = 1
    ENCODER_INNER_CCW_1 = 2
    ENCODER_OUTER_CW_1 = 4
    ENCODER_OUTER_CCW_1 = 8
    ENCODER_INNER_CW_2 = 16
    ENCODER_INNER_CCW_2 = 32
    ENCODER_OUTER_CW_2 = 64
    ENCODER_OUTER_CCW_2 = 128


def radio1_states():
    return {
        RadioPanelFlag.COM1_1,
        RadioPanelFlag.COM2_1,
        RadioPanelFlag.NAV1_1,
        RadioPanelFlag.NAV2_1,
        RadioPanelFlag.ADF_1,
        RadioPanelFlag.DME_1,
        RadioPanelFlag.XPDR_1
    }


def radio2_states():
    return {
        RadioPanelFlag.COM1_2,
        RadioPanelFlag.COM2_2,
        RadioPanelFlag.NAV1_2,
        RadioPanelFlag.NAV2_2,
        RadioPanelFlag.ADF_2,
        RadioPanelFlag.DME_2,
        RadioPanelFlag.XPDR_2
    }


def is_radiox_state(state, radiox_states):
    for s in radiox_states:
        if s == state:
            return True
    return False


class RadioPanelLcd(IntEnum):
    # Byte offsets per LCD
    LCD1 = 0
    LCD2 = 5
    LCD3 = 10
    LCD4 = 15
