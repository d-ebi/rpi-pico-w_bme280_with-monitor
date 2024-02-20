from array import array

import fonts
import view

# FONT_WIDTH
f_w = view.f_w
unscii16 = view.unscii16

def show_pres(oled, pres_int, pres_decimal):
    x_s = 13
    y_s = 25
    # 整数部
    for i, e in enumerate(list(pres_int)):
        c = unscii16[ord(e) - fonts.ASCII_START]
        fonts.add_text_to_oled(oled, c, f_r=2, x_s=i*f_w+x_s, y_s=y_s)
    # 小数部
    pd = fonts.get_unscii16(unscii16, pres_decimal)
    fonts.add_text_to_oled(oled, pd, x_s=69+x_s, y_s=38)
    # hPa
    hpa_x_s = 78
    for i, e in enumerate(list('hPa')):
        c = unscii16[ord(e) - fonts.ASCII_START]
        fonts.add_text_to_oled(oled, c, x_s=i*int(f_w/2)+hpa_x_s+x_s, y_s=38)
    # 小数点
    oled.rect(65+x_s, 49, 2, 2, 1, True)

def show_home(oled):
    # 屋根
    poly = array('h', (98, 15, 124, 15, 111, 2))
    oled.poly(1, 1, poly, 2, True)
    # 壁
    poly = array('h', (102, 16, 120, 16, 120, 28, 102, 28))
    oled.poly(1, 1, poly, 1, True)
    # ドア
    poly = array('h', (108, 18, 114, 18, 114, 28, 108, 28))
    oled.poly(1, 1, poly, 0, True)
