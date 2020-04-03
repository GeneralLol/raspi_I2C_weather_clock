#! /usr/bin/python3
import subprocess
import time
import datetime
import threading

import weatherHandler
import displayHandler

import RPi.GPIO as GPIO

def main():
    DATE_FORMAT = '%Y-%m-%d %a'
    TIME_FORMAT = '%H:%M:%S '

    weather = weatherHandler.cityWeather(refreshInterval=5, cityID="5083221"); 
    display = displayHandler.SerialOLEDDisplay(128, 64)
    dt = datetime.datetime.now()

    weatherMonitor = threading.Thread(group=None, name="weather monitor", \
                                        target=weather_monitor, \
                                        args=(weather, weather.refreshInterval)
                                        )
    datetimeMonitor = threading.Thread(group=None, name="datetime monitor", \
                                        target=datetime_monitor, \
                                        args=(dt,)\
                                        )

    displayMonitor = threading.Thread(group=None, name="display_monitor", \
                                        target=display_monitor, \
                                        kwargs={"display":display, "weather":weather, "dt":dt, \
                                                "DATE_FORMAT":DATE_FORMAT, "TIME_FORMAT":TIME_FORMAT}\
                                        )
    
    weatherMonitor.start()
    datetimeMonitor.start()
    displayMonitor.start()

    while (True):
        time.sleep(100000000)
    

def weather_monitor(weather, sleepTime):
    while (True):
        weather.check_refresh()

        time.sleep(sleepTime)

def datetime_monitor(dt, sleepTime=1):
    while (True):
        dt = datetime.datetime.now()
        
        time.sleep(sleepTime)

def display_monitor(display, weather, dt, DATE_FORMAT, TIME_FORMAT, sleepTime=1):
    while (True): 
        #Take all data out of objects
        dateStr = dt.date().strftime(DATE_FORMAT)
        timeStr = dt.time().strftime(TIME_FORMAT)

        wthr = weather.weather
        temp = weather.temp
        humidity = weather.humidity

        #Draw things onto the display (basically hard-coding)
        display.clear_buffer()
        (x, y) = (0, 0)
        nextAvailable = display.add_string(x, y, dateStr, fontSize=13)
        (x, y) = nextAvailable[3]
        nextAvailable = display.add_string(x, y, timeStr, fontSize=17)
        (x, y) = nextAvailable[3]
        nextAvailable = display.add_string(x, y, wthr, fontSize=25)
        (x, y) = nextAvailable[1]
        x += 10
        nextAvailable = display.add_string(x, y, temp, fontSize=15)
        (x, y) = nextAvailable[3]
        nextAvailable = display.add_string(x, y, humidity, fontSize=10)
        display.display_everything()

        time.sleep(sleepTime)

if (__name__ == "__main__"):
    main()