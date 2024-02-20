from array import array
import fonts

# FONT_WIDTH
f_ws = 8
f_w  = 16
unscii16 = fonts.load_unscii16()

def show_temp(oled, temp_int, temp_decimal):
    y_s = -4
    # 整数部
    for i, e in enumerate(list(temp_int)):
        c = fonts.get_unscii16(unscii16, e)
        fonts.add_text_to_oled(oled, c, f_r=2, x_s=i*f_w, y_s=y_s)
    # 小数部
    td = fonts.get_unscii16(unscii16, temp_decimal)
    fonts.add_text_to_oled(oled, td, x_s=37, y_s=9)
    # ℃
    fonts.add_text_to_oled(oled, fonts.DEGREE_CELSIUS_SYMBOL, f_r=1, x_s=36, y_s=y_s-1)
    # 小数点
    oled.rect(33, 20, 2, 2, 1, True)

def show_hum(oled, hum):
    x_s = 52
    y_s = -4
    # 整数部
    for i, e in enumerate(list(hum)):
        c = unscii16[ord(e) - fonts.ASCII_START]
        fonts.add_text_to_oled(oled, c, f_r=2, x_s=i*f_w+x_s, y_s=y_s)
    # %
    per = fonts.get_unscii16(unscii16, '%')
    fonts.add_text_to_oled(oled, per, x_s=84, y_s=8)

def show_pagination(oled, page):
    oled.hline(0, 55, 128, 1)
    for i in range(0, 4):
        is_fill = (page == i)
        oled.rect((i * 6) + 53, 58, 4, 4, 1, is_fill)

def show_thermometer_lines(oled):
    oled.line(48, 0, 48, 25, 1)
    oled.line(94, 0, 94, 34, 1)
    oled.line(94, 34, 128, 34, 1)
    oled.line(0, 25, 94, 25, 1)

