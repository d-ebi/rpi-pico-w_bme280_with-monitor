import gc
import json
import machine
import network
import os
import socket
import time
import uasyncio
import utime
import urequests
from array import array
from machine import I2C, Pin

from bme280 import BME280
from microdot_asyncio import Microdot
from ssd1306 import SSD1306_I2C

import html
import oled_text
import open_weather_map
import settings
import view
from led import LED
from view import house, outdoor, clock, infos

SW1_PIN  = 15
SW2_PIN  = 14
SW3_PIN  = 13
SW4_PIN  = 12
LED_PIN  = 0
RES_PIN  = 22
I2C_CH   = 1
I2C_SDA  = 26
I2C_SCL  = 27
I2C_FREQ = 400000
OLED_WIDTH  = 128
OLED_HEIGHT = 64
FONT_SIZE   = 8

# init
i2c     = I2C(I2C_CH, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=I2C_FREQ)
bme280  = BME280(i2c=i2c)
oled    = None
sta_if  = None
led     = LED(LED_PIN)
owm_values   = ()
current_page = 0
unixtime     = 0
start_time   = 0.0

"""events"""
def write_log(l, t):
    with open('main.log', 'a') as f:
        f.write(f'[{l}]:{unixtime},{t}\n')

def write_error_log(e, func):
    pass
    # qualname = getattr(e, '__qualname__', '')
    # write_log('ERROR', f'{qualname},{e.value},in {func}')

def __get_temp(ts):
    t_int, t_decimal = ts.split('.')
    return (f'{t_int:>2s}', t_decimal[0])

def __get_press(ps):
    p = ps.split('.')
    p_int = f'{p[0]:>4s}'
    if len(p) == 1:
        return (p_int)
    return (p_int, p[0][0])

def __get_hum(hs):
    h= hs.split('.')[0]
    return f'{h:>2s}' if int(h) < 100 else '99'

def show_bme280_values():
    ts, ps, hs = bme280.values
    t_int, t_decimal = __get_temp(ts)
    p_int, p_decimal = __get_press(ps)
    h = __get_hum(hs)
    oled.fill(0)
    view.show_temp(oled, t_int, t_decimal)
    view.show_hum(oled, h)
    house.show_pres(oled, p_int, p_decimal)
    house.show_home(oled)
    view.show_thermometer_lines(oled)
    view.show_pagination(oled, current_page)
    oled.show()

def show_outdoor_values():
    if not owm_values:
        return
    ts, ps, hs = owm_values
    t_int, t_decimal = __get_temp(ts)
    p = __get_press(ps)
    h = __get_hum(hs)
    oled.fill(0)
    view.show_temp(oled, t_int, t_decimal)
    view.show_hum(oled, h)
    outdoor.show_pres(oled, p)
    outdoor.show_tree(oled)
    view.show_thermometer_lines(oled)
    view.show_pagination(oled, current_page)
    oled.show()

def show_clock():
    if not unixtime:
        return
    y, m, d, H, M, S, dow, _ = time.localtime(unixtime)
    oled.fill(0)
    clock.show_date(oled, y, m, d, dow)
    clock.show_time(oled, H, M, S)
    clock.show_clock_lines(oled)
    view.show_pagination(oled, current_page)
    oled.show()

def show_settings():
    if not sta_if.isconnected():
        return
    oled.fill(0)
    infos.show(oled, sta_if.config('ssid'), sta_if.ifconfig()[0])
    view.show_pagination(oled, current_page)
    oled.show()

def fetch_timestamp():
    global unixtime
    gc.collect()
    url = 'https://worldtimeapi.org/api/ip'
    r = None
    r = urequests.get(url)
    u = r.json()['unixtime']
    r.close()
    gc.collect()
    return u

"""toggle button evnets"""
def sw1_event(e):
    global current_page
    current_page = 0

def sw2_event(e):
    global current_page
    current_page = 1

def sw3_event(e):
    global current_page
    current_page = 2

def sw4_event(e):
    global current_page
    current_page = 3

"""async proccesses"""
proccess = [show_bme280_values, show_outdoor_values, show_clock, show_settings]

async def show_process():
    try:
        while True:
            proccess[current_page]()
            await uasyncio.sleep(0.8)
    except Exception as e1:
        write_error_log(e1, 'show_process')
        qualname = getattr(e, '__qualname__', 'No qualname')
        oled_text.stream(oled, f'{qualname}:{e1.value}')
        led.on(LED.VERY_HIGH)

async def fetch_weather():
    global owm_values, sta_if
    r = 0 # retry_count
    l = 3 # max_retry_count
    while not sta_if:
        await uasyncio.sleep(1)
    while not sta_if.isconnected():
        await uasyncio.sleep(1)
    while True:
        try:
            owm_values = open_weather_map.fetch_current(settings.open_weather_map_api_key, settings.lat, settings.lon)
            await uasyncio.sleep(600)
        except Exception as e:
            gc.collect()
            if r < l:
                await uasyncio.sleep(60)
            else:
                write_error_log(e, 'fetch_weather')
                await uasyncio.sleep(60)
            r += 1
            continue

async def update_unixtime():
    global start_time, unixtime
    re_c = 0
    max_re_c = 3
    while not sta_if:
        await uasyncio.sleep(1)
    while not sta_if.isconnected():
        await uasyncio.sleep(1)
    interval   = float(0)
    start_time = time.time()
    while True:
        try:
            if interval == 0:
                unixtime = fetch_timestamp() + (9*3600) - 6
            interval += 0.5
            if interval == 3600:
                interval = 0
            unixtime += (round(time.time() - start_time))
            start_time = time.time()
            await uasyncio.sleep(0.5)
        except Exception as e:
            write_error_log(e, 'update_unixtime')
            await uasyncio.sleep(10)
            machine.soft_reset()

async def server():
    ct_json = {'Content-Type':'application/json'}
    app = Microdot()
    @app.get('/')
    async def index(_):
        return html.index,{'Content-Type':'text/html'}
    @app.get('/api/1/bme280')
    async def get_bme280_values(_):
        t, p, h = bme280.values
        return {'temp':t,'pres':p,'hum':h},ct_json
    @app.get('/api/1/log')
    async def get_log(_):
        with open('/main.log', 'r') as f:
            l = f.read()
        return l,{'Content-Type':'text/plain'}
    @app.delete('/api/1/log')
    async def clear_log(_):
        with open('/main.log', 'w') as f:
            f.write('')
        return {'status':200},ct_json
    @app.get('/api/1/page')
    async def get_current_page(_):
        return {'current_page':current_page}
    @app.put('/api/1/page/<int:page_num>')
    async def change_current_page(_, page_num):
        if 0 <= page_num < 4:
            global current_page
            current_page = page_num
            return {'status':200,'current_page':current_page},ct_json
        else:
            return {'status':400,'message':'Out of range.'},ct_json
    app.run(port=80)

"""sync proccesses"""
def reset_oled():
    global oled
    reset = Pin(RES_PIN, Pin.OUT)
    reset.low()
    time.sleep(0.1)
    reset.high()
    oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

def connect_sta_if():
    global sta_if
    retry_count = 0
    max_retry_count = 15

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        led.on(LED.MEDIUM)
        sta_if.active(True)
        sta_if.connect(settings.ssid, settings.password)
        while not sta_if.isconnected():
            if max_retry_count < retry_count:
                led.on(LED.VERY_HIGH)
                write_log('CRITICAL', 'Wi-Fi connection failure. Do machine.reset().')
                machine.reset()
            led.on(LED.MEDIUM)
            time.sleep(1)
            led.off()
            time.sleep(1)
            retry_count += 1
        led.off()

def attach_tactswitch_events():
    sw1 = Pin(SW1_PIN, Pin.IN, Pin.PULL_DOWN)
    sw2 = Pin(SW2_PIN, Pin.IN, Pin.PULL_DOWN)
    sw3 = Pin(SW3_PIN, Pin.IN, Pin.PULL_DOWN)
    sw4 = Pin(SW4_PIN, Pin.IN, Pin.PULL_DOWN)
    sw1.irq(trigger=Pin.IRQ_FALLING, handler=sw1_event)
    sw2.irq(trigger=Pin.IRQ_FALLING, handler=sw2_event)
    sw3.irq(trigger=Pin.IRQ_FALLING, handler=sw3_event)
    sw4.irq(trigger=Pin.IRQ_FALLING, handler=sw4_event)

async def main():
    task1 = uasyncio.create_task(show_process())
    task2 = uasyncio.create_task(fetch_weather())
    task3 = uasyncio.create_task(update_unixtime())
    task4 = uasyncio.create_task(server())
    await task1
    await task2
    await task3
    await task4

if __name__ == '__main__':
    try:
        connect_sta_if()
        reset_oled()
        led.off()
        attach_tactswitch_events()
        uasyncio.run(main())
    except Exception as e:
        write_error_log(e, '__main__')
