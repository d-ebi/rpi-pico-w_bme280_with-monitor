import gc
import urequests


def fetch_current(api_key, lat, lon):
    gc.collect()
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
    r = None
    r = urequests.get(url)
    j = r.json()['main']
    r.close()
    gc.collect()
    return (str(j['temp']), str(j['pressure']), str(j['humidity']))
