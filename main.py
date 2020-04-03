#! /usr/bin/python3
import subprocess
import time
import datetime

import weatherHandler
import displayHandler

import RPi.GPIO as GPIO

def main():
    DATE_FORMAT = '%Y-%m-%d %a'
    TIME_FORMAT = '%H:%M:%S '

    weather = weatherHandler.cityWeather(refreshInterval=5, cityID="5083221"); 
    display = displayHandler.SerialOLEDDisplay(128, 64)

    while (True):
        currentDatetime    = datetime.datetime.now()
        currentDateStr = currentDatetime.date().strftime(DATE_FORMAT)
        currentTimeStr = currentDatetime.time().strftime(TIME_FORMAT)
        currentWeather     = weather.get_current_weather()
        currentTemperature = weather.get_current_temperature()
        currentHumidity    = weather.get_current_humidity()

        #Print everything out for debug purposes
        debug_str = "{}\n{}\n{}\n{}\n{}\n\n".format(\
                                            currentDateStr, \
                                            currentTimeStr, \
                                            currentWeather, \
                                            currentTemperature, \
                                            currentHumidity)
        print(debug_str)

        #Draw things onto the display (basically hard-coding)
        display.clear_buffer()
        (x, y) = (0, 0)
        nextAvailable = display.add_string(x, y, currentDateStr, fontSize=13)
        (x, y) = nextAvailable[3]
        nextAvailable = display.add_string(x, y, currentTimeStr, fontSize=17)
        (x, y) = nextAvailable[3]
        nextAvailable = display.add_string(x, y, currentWeather, fontSize=25)
        (x, y) = nextAvailable[1]
        x += 10
        nextAvailable = display.add_string(x, y, currentTemperature, fontSize=15)
        (x, y) = nextAvailable[3]
        nextAvailable = display.add_string(x, y, currentHumidity, fontSize=10)
        display.display_everything()

        time.sleep(0.5)

def weather_monitor():
    pass

def datetime_monitor():
    pass


if (__name__ == "__main__"):
    main()