from micropython import const
from machine import Pin, I2C
import lvesp32
import lvgl as lv

FT_ADDR = const(0x38)
FT_INT_PIN = const(39)


class ft6336u:
    def __init__(self):

        # Initializations
        self.i2c = I2C(1, sda=Pin(21), scl=Pin(22), freq=100000)
        self.int = Pin(FT_INT_PIN, Pin.IN)

        disp = lv.disp_t.cast(None)
        self.screen_width = disp.get_hor_res()
        self.screen_height = disp.get_ver_res()

        indev_drv = lv.indev_drv_t()
        indev_drv.init()
        indev_drv.type = lv.INDEV_TYPE.POINTER
        indev_drv.read_cb = self.read
        indev_drv.register()

        self.reg_write_byte(0xA4, b"\x00")

    def is_pressed(self):
        return not self.int.value()

    def reg_write_byte(self, reg, value):
        self.i2c.writeto_mem(FT_ADDR, reg, value)

    def reg_read_byte(self, reg):
        return self.i2c.readfrom_mem(FT_ADDR, reg, 1)

    def reg_read_multiple(self, reg, size):
        return self.i2c.readfrom_mem(FT_ADDR, reg, size)

    def get_coords(self):

        # Abort if not pressed
        if not self.is_pressed():
            return

        # Get data and number of touches
        data = self.reg_read_multiple(0x02, 11)
        touches = data[0]

        if touches > 2:
            return

        # Get coordinates
        x = ((data[1] << 8) | data[2]) & 0x0FFF
        y = ((data[3] << 8) | data[4]) & 0x0FFF

        return (x, y)

    def read(self, indev_drv, data) -> int:

        coords = self.get_coords()

        if coords:
            data.point.x, data.point.y = coords
            data.state = lv.INDEV_STATE.PR
            return False
        data.state = lv.INDEV_STATE.REL
        return False
