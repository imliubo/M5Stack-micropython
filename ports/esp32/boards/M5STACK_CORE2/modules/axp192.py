"""
MIT License

Copyright (c) 2020 IAMLIUBO

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from machine import I2C, Pin
from micropython import const
import ustruct

#                      IO0   IO1   IO2   IO3   IO4
GPIOx_MODE_REG_LIST = [0x90, 0x92, 0x93, 0x95, 0x95]
GPIOx_REWR_REG_LIST = [0x94, 0x94, 0x94, 0x96, 0x96]
GPIOx_RE_VAL_OFFSET = [4, 5, 6, 4, 5]
GPIOx_WR_VAL_OFFSET = [0, 1, 2, 0, 1]

#                           DC1   DC2   DC3
DC_VOL_SET_REG_LIST = [-1, 0x26, 0x23, 0x27]
DC_ENABLE_OFFSET = [-1, 0x00, 0x04, 0x01]

GPIO0_MODE_LIST = {
    0: const(0b101),
    1: const(-1),
    2: const(0b001),
    3: const(0b010),
    4: const(0b100),
    5: const(0b111),
    6: const(0b000),
    7: const(-1),
    8: const(-1),
}

GPIO1_2_MODE_LIST = {
    0: const(0b101),
    1: const(-1),
    2: const(0b001),
    3: const(-1),
    4: const(0b100),
    5: const(0b111),
    6: const(0b000),
    7: const(0b010),
    8: const(-1),
}

GPIO3_MODE_LIST = {
    0: const(-1),
    1: const(-1),
    2: const(0b010),
    3: const(-1),
    4: const(-1),
    5: const(-1),
    6: const(0b001),
    7: const(-1),
    8: const(0b000),
}

GPIO4_MODE_LIST = {
    0: const(-1),
    1: const(-1),
    2: const(0b010),
    3: const(-1),
    4: const(0b011),
    5: const(-1),
    6: const(0b001),
    7: const(-1),
    8: const(0b000),
}

GPIOx_MODE_LIST = [
    GPIO0_MODE_LIST,
    GPIO1_2_MODE_LIST,
    GPIO1_2_MODE_LIST,
    GPIO3_MODE_LIST,
    GPIO4_MODE_LIST,
]

GPIO_MODE_STR_LIST = [
    "OUTPUT_LOW_MODE",
    "OUTPUT_HIGH_MODE",
    "INPUT_MODE",
    "LDO_MODE",
    "ADC_MODE",
    "FLOATING_MODE",
    "OPEN_DRAIN_OUTPUT_MODE",
    "PWM_OUTPUT_MODE",
    "EXTERN_CHARGING_CTRL_MODE",
]


class AXP192(object):

    # GPIO LIST
    GPIO0 = const(0)
    GPIO1 = const(1)
    GPIO2 = const(2)
    GPIO3 = const(3)
    GPIO4 = const(4)

    # GPIO MODE LIST
    IO_OUTPUT_LOW_MODE = const(0)
    IO_OUTPUT_HIGH_MODE = const(1)
    IO_INPUT_MODE = const(2)
    IO_LDO_MODE = const(3)
    IO_ADC_MODE = const(4)
    IO_FLOATING_MODE = const(5)
    IO_OPEN_DRAIN_OUTPUT_MODE = const(6)
    IO_PWM_OUTPUT_MODE = const(7)
    IO_EXTERN_CHARGING_CTRL_MODE = const(8)

    # BAT charge current
    BAT_100MA = const(0b0000)
    BAT_190MA = const(0b0001)
    BAT_280MA = const(0b0010)
    BAT_360MA = const(0b0011)
    BAT_450MA = const(0b0100)
    BAT_550MA = const(0b0101)
    BAT_630MA = const(0b0110)
    BAT_700MA = const(0b0111)

    # BAT charge voltage
    BAT_4100MV = const(0b00)
    BAT_4150MV = const(0b01)
    BAT_4200MV = const(0b10)
    BAT_4360MV = const(0b11)

    # BACK BAT charge current
    BACK_BAT_50UA = const(0b00)
    BACK_BAT_100UA = const(0b01)
    BACK_BAT_200UA = const(0b10)
    BACK_BAT_400UA = const(0b11)

    # BACK BAT charge voltage
    BACK_BAT_3100MV = const(0b00)
    BACK_BAT_3000MV = const(0b01)
    BACK_BAT_2500MV = const(0b11)

    def __init__(self, addr=0x34, debug=False):
        self.addr = addr
        self.debug = debug
        self.i2c = I2C(1, sda=Pin(21), scl=Pin(22), freq=400000)

    def check_id(self):
        return self._read_byte(0x03)

    def limit_off(self):
        val = self._read_byte(0x30)
        val &= ~(1 << 1)
        self._write_byte(0x30, val)

    # AXP192 gpio mode set.
    def set_gpio_mode(self, gpio, mode):
        if gpio < 0 or gpio > 4:
            return
        if mode < 0 or mode > 8:
            return
        s_mode = GPIOx_MODE_LIST[gpio][mode]
        if s_mode < 0:
            return
        val = self._read_byte(GPIOx_MODE_REG_LIST[gpio])
        if gpio == 0 or gpio == 1 or gpio == 2:
            val &= 0xF8
        if gpio == 3:
            val &= 0xFC
        if gpio == 4:
            val &= 0xF3
        val |= s_mode
        if self.debug:
            print("GPIO: {} Mode: {}".format(gpio, GPIO_MODE_STR_LIST[val]))
        self._write_byte(GPIOx_MODE_REG_LIST[gpio], val)

    # Read the gpio value.
    def gpio_read(self, gpio):
        if gpio < 0 or gpio > 4:
            return
        val = self._read_byte(GPIOx_REWR_REG_LIST[gpio])
        mask = 1 << GPIOx_RE_VAL_OFFSET[gpio]
        if self.debug:
            print("GPIO: {} Read: {}".format(gpio, (val & mask)))
        return val & mask

    # Write gpio value.
    def gpio_write(self, gpio, value):
        if gpio < 0 or gpio > 4:
            return
        if value < 0 or value > 1:
            return
        val = self._read_byte(GPIOx_REWR_REG_LIST[gpio])
        if value:
            if self.debug:
                print("GPIO: {} Write: {}".format(gpio, value))
            val |= 1 << GPIOx_WR_VAL_OFFSET[gpio]
        else:
            if self.debug:
                print("GPIO: {} Write: {}".format(gpio, value))
            val &= ~(1 << GPIOx_WR_VAL_OFFSET[gpio])
        self._write_byte(GPIOx_REWR_REG_LIST[gpio], val)

    # Set the DCDC output voltage.
    def set_dc_voltage(self, dc, vol):
        """
                vol range    step  current
        DCDC1: 0.7v ~ 3.5v   25mv   1.2A
        DCDC2: 0.7v ~ 2.275v 25mv   1.6A
        DCDC3: 0.7v ~ 3.5v   25mv   0.7A
        """
        if dc < 1 or dc > 3:
            return
        vol_mv = vol * 1000
        if vol_mv < 700:
            vol_mv = 700
        if dc == 2 and vol_mv > 2275:
            vol_mv = 2275
        if (dc == 1 or dc == 3) and vol_mv > 3500:
            vol_mv = 3500
        if self.debug:
            print("DC: {} voltage:  {}mv".format(dc, vol_mv))
        self._write_byte(DC_VOL_SET_REG_LIST[dc], int(((vol_mv - 700) // 25)))

    # Enable the DCDC output.
    def dc_enable(self, dc, value):
        """
        value:
            0  disable
            1  enable
        """
        if dc < 1 or dc > 3:
            return
        val = self._read_byte(0x12)
        if value:
            if self.debug:
                print("DC: {} enable".format(dc))
            val |= 1 << DC_ENABLE_OFFSET[dc]
        else:
            if self.debug:
                print("DC: {} disable".format(dc))
            val &= ~(1 << DC_ENABLE_OFFSET[dc])
        self._write_byte(0x12, val)

    # Set LDO output voltage.
    def set_ldo_voltage(self, ldo, vol):
        """
               vol range   step    current
        LDO1:    RTC                30ma
        LDO2: 1.8v ~ 3.3v  100mv    200ma
        LDO3: 1.8v ~ 3.3v  100mv    200ma
        """
        if ldo < 2 or ldo > 3:
            return
        vol_mv = vol * 1000
        if vol_mv < 1800:
            vol_mv = 1800
        if vol_mv > 3300:
            vol_mv = 3300
        val = self._read_byte(0x28)
        if ldo == 2:
            if self.debug:
                print("LDO: {} volatge: {}mv".format(ldo, vol_mv))
            val = (val & 0x0F) | (int(((vol_mv - 1800) // 100)) << 4)
        if ldo == 3:
            if self.debug:
                print("LDO: {} volatge: {}mv".format(ldo, vol_mv))
            val = (val & 0xF0) | int(((vol_mv - 1800) // 100))
        self._write_byte(0x28, val)

    # Enable LDO output.
    def ldo_enable(self, ldo, value):
        if ldo < 2 or ldo > 3:
            return
        val = self._read_byte(0x12)
        if value:
            if self.debug:
                print("LDO: {} enable".format(ldo))
            val |= 1 << ldo
        else:
            if self.debug:
                print("LDO: {} enable".format(ldo))
            val &= ~(1 << ldo)
        self._write_byte(0x12, val)

    # Set the battery charging current.
    def set_bat_charge_current(self, current):
        if current < 0 or current > 7:
            return
        val = self._read_byte(0x33)
        val = (val & 0xF0) | (current & 0x0F)
        self._write_byte(0x33, val)

    def set_bat_charge_voltage(self, vol):
        if vol < 0 or vol > 3:
            return
        val = self._read_byte(0x33)
        val = (val & 0x8F) | (vol & 0x60)
        self._write_byte(0x33, val)

    def bat_charget_enable(self, value):
        val = self._read_byte(0x33)
        if value:
            val |= 1 << 7
        else:
            val &= ~(1 << 7)
        self._write_byte(0x33, val)

    def set_back_bat_charge_current(self, current):
        if current < 0 or current > 3:
            return
        val = self._read_byte(0x35)
        val = (val & 0xFC) | (current & 0x03)
        self._write_byte(0x35, val)

    def set_back_bat_charge_voltage(self, vol):
        if vol < 0 or vol > 3:
            return
        val = self._read_byte(0x35)
        val = (val & 0x9F) | (vol & 0x60)
        self._write_byte(0x35, val)

    def back_bat_charget_enable(self, value):
        val = self._read_byte(0x35)
        if value:
            val |= 1 << 7
        else:
            val &= ~(1 << 7)
        self._write_byte(0x35, val)

    # Turn off all power output.
    def power_off(self):
        val = self._read_byte(0x32)
        val |= 1 << 7
        self._write_byte(0x32, val)

    """
    I2C write & read function
    """

    def _write_byte(self, reg, data):
        buf = bytearray(1)
        ustruct.pack_into("<b", buf, 0, data)
        self.i2c.writeto_mem(self.addr, reg, buf)

    def _read_byte(self, reg):
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]
