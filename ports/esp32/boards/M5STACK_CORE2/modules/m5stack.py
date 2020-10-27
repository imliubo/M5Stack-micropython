'''
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
'''
from axp192 import AXP192

class M5Stack(object):

    def __init__(self):
        self.axp = AXP192()

    def power_on(self):
        # GPIO1 & GPIO2 & GPIO4 set OD mode
        self.axp.gpio_mode_set(self.axp.GPIO1, self.axp.IO_OPEN_DRAIN_OUTPUT_MODE)
        self.axp.gpio_mode_set(self.axp.GPIO2, self.axp.IO_OPEN_DRAIN_OUTPUT_MODE)
        self.axp.gpio_mode_set(self.axp.GPIO4, self.axp.IO_OPEN_DRAIN_OUTPUT_MODE)

        # GPIO1 Power LED
        self.axp.gpio_write(self.axp.GPIO1, 0)

        # DCDC1 3.3V => ESP32
        self.axp.dc_voltage_set(1, 3.3)
        self.axp.dc_enable(1, 1)

        # DCDC3 3V => LCD Backlight
        self.axp.dc_voltage_set(3, 3)
        self.axp.dc_enable(1, 1)

        # LDO2 3.3V => LCD, SD
        self.axp.ldo_voltage_set(2, 3.3)
        self.axp.ldo_enable(2, 1)

        # LDO3 2V => motor
        self.axp.ldo_voltage_set(3, 2)

        # BAT charge current 100MA
        self.axp.back_bat_charge_current_set(self.axp.BAT_190MA)

    def power_off(self):
        self.axp.power_off()

    def power_led(self, state):
        if state:
            self.axp.gpio_write(self.axp.GPIO1, 0)
        else:
            self.axp.gpio_write(self.axp.GPIO1, 1)
         