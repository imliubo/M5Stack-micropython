import gc
import uos
from flashbdev import bdev

try:
    if bdev:
        uos.mount(bdev, "/")
except OSError:
    import inisetup

    vfs = inisetup.setup()

from m5stack import M5Stack

m5 = M5Stack()

scr = m5.lv.scr_act()

heard_label = m5.lv.label(scr)
heard_label.set_text("M5Stack Core2")
style = m5.lv.style_t()
style.set_text_font(m5.lv.STATE.DEFAULT, m5.lv.font_montserrat_28)
heard_label.add_style(heard_label.PART.MAIN, style)
heard_label.align(m5.lv.scr_act(), m5.lv.ALIGN.IN_TOP_MID, 0, 5)

btn = m5.lv.btn(scr)
btn.align(m5.lv.scr_act(), m5.lv.ALIGN.CENTER, 0, 0)
btn_label = m5.lv.label(btn)
btn_label.set_text("Press me :)")

info_label = m5.lv.label(scr)
info_label.set_recolor(True)
info_label.set_text("Power by #FF0000 micropython# & #FF0000 lvgl#")
info_label.align(m5.lv.scr_act(), m5.lv.ALIGN.IN_BOTTOM_MID, 0, -5)


def btn_callback(obj, event):
    if event == m5.lv.EVENT.PRESSED:
        m5.power_led(False)
        m5.vibration(True)
    elif event == m5.lv.EVENT.RELEASED:
        m5.power_led(True)
        m5.vibration(False)


btn.set_event_cb(btn_callback)

# Load the screen
m5.lv.scr_load(scr)

gc.collect()
