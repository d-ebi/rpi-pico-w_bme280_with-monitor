import fonts
import view

DAY_OF_WEEK = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
# FONT_WIDTH
f_w  = view.f_w
f_ws = view.f_ws
unscii16 = view.unscii16

def show_date(oled, y, m, d, dow):
    ds = f'{y}/{m:02}/{d:02} {DAY_OF_WEEK[dow]}.'
    x_s = 5
    y_s = 2
    for i, e in enumerate(list(ds)):
        c = unscii16[ord(e) - fonts.ASCII_START]
        fonts.add_text_to_oled(oled, c, f_r=1, x_s=i*f_ws+x_s, y_s=y_s)

def show_clock_lines(oled):
    oled.hline(0, 18, 128, 1)

def show_time(oled, H, M, S):
    dt = f'{H:02}:{M:02}'
    x_s = 13
    y_s = 22
    # hour:minutes
    for i, e in enumerate(list(dt)):
        c = unscii16[ord(e) - fonts.ASCII_START]
        fonts.add_text_to_oled(oled, c, f_r=2, x_s=i*f_w+x_s, y_s=y_s)
    # second
    s = f'{S:02}'
    x_s_s = 99
    y_s_s = 35
    for i, e in enumerate(list(s)):
        c = unscii16[ord(e) - fonts.ASCII_START]
        fonts.add_text_to_oled(oled, c, f_r=1, x_s=i*f_ws+x_s_s, y_s=y_s_s)
