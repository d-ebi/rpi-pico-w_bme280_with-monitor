ASCII_START = 32
ASCII_END = 126
DEGREE_CELSIUS_SYMBOL = f'{int("c0de33303030331e000000", 16):0128b}'

def load_unscii16():
    unscii16_chars = list()
    with open('/fonts/unscii-16-minimal.hex', 'r') as f:
        tmp = (e.split(':')[-1].replace('\n', '') for e in f.readlines())
        unscii16_chars = [f'{int(e, 16):0128b}' for e in tmp]
    return unscii16_chars

def get_unscii16(unscii16, s):
    return unscii16[ord(s) - ASCII_START]

def add_text_to_oled(ssd13xx, c, f_r=1, f_w=8, x_s=0, y_s=0):
    """
    f_r: font_ratio フォントの倍率,デフォルトが8pxでf_r=2なら16px
    f_w: font_width フォントの横幅(px)
    x_s: x_shift    表示開始位置
    y_s: y_shift    表示開始位置
    """

    for i in range(0, len(c)):
        if (c[i] == '0'):
            continue
        x_pointer = (i % f_w)
        y_pointer = int(i / f_w)
        x = x_pointer + x_pointer * (f_r - 1) + x_s
        y = y_pointer + y_pointer * (f_r - 1) + y_s
        ssd13xx.rect(x, y, f_r, f_r, 1, True)

