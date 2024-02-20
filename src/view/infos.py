import view

# FONT_WIDTH
f_ws = view.f_ws

def show(oled, ssid, ip):
    l   = 1
    lw  = 16
    y_s = 4
    oled.text('SSID:', 0, 0)

    st = ssid[:lw*2]
    ss = [st[i:i+lw] for i in range(0, len(st), lw)]
    for t in ss:
        oled.text(t, 0, l*f_ws)
        l += 1
    oled.text('IP Address:', 0, l*f_ws+y_s)
    l += 1
    oled.text(ip, 0, l*f_ws+y_s)
