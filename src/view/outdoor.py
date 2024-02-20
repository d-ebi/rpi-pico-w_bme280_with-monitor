from array import array

import fonts
import view

# FONT_WIDTH
f_w = view.f_w
unscii16 = view.unscii16

def show_pres(oled, pres_int):
    x_s = 20
    y_s = 25
    # 整数部
    for i, e in enumerate(list(pres_int)):
        c = unscii16[ord(e) - fonts.ASCII_START]
        fonts.add_text_to_oled(oled, c, f_r=2, x_s=i*f_w+x_s, y_s=y_s)
    # hPa
    hpa_x_s = 65
    for i, e in enumerate(list('hPa')):
        c = unscii16[ord(e) - fonts.ASCII_START]
        fonts.add_text_to_oled(oled, c, x_s=i*int(f_w/2)+hpa_x_s+x_s, y_s=38)

def show_tree(oled):
    # 円
    oled.ellipse(112, 10, 10, 10, 1, True)
    # 幹
    oled.rect(111, 13, 3, 15, 1, True)
    # 根
    oled.rect(102, 28, 21, 3, 1, True)
