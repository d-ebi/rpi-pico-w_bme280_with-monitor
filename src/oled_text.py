from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

FONT_SIZE = 8
WIDTH = 128

def add_texts(oled, texts):
    oled.fill(0)
    for i, t in enumerate(texts):
        oled.text(t, 0, i * FONT_SIZE)


def stream(oled, text):
    oled.fill(0)
    text_width = WIDTH / FONT_SIZE
    start = 0
    charactor_limit = int(WIDTH / FONT_SIZE)
    line_length = int(len(text) / charactor_limit)

    while (start / charactor_limit) <= line_length:
        end = start + charactor_limit
        line = int(end / charactor_limit) * FONT_SIZE - FONT_SIZE
        oled.text(text[start:end], 0, line)
        start = end
    oled.show()
