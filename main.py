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

        #If the time is between 7pm and 8am, dim the display. 
        if (currentDatetime.time() < datetime.time(hour=8) or \
            currentDatetime.time() > datetime.time(hour=19)):
            display.config_brightness(0)
        else:
            display.config_brightness(255)

        #Draw things onto the display (basically hard-coding)
        display.clear_buffer()
        (x, y) = (0, 0)
        nextAvailable = display.add_string(x, y, 128, 13, currentDateStr, fontSize=13)
        (x, y) = nextAvailable[3]
        nextAvailable = display.add_string(x, y, 128, 30, currentTimeStr, fontSize=17)
        (x, y) = nextAvailable[3]
        nextAvailable = display.add_string(x, y, 90, 64, currentWeather, fontSize=25)
        (x, y) = nextAvailable[1]
        x = 90
        nextAvailable = display.add_string(x, y, 128, 47, currentTemperature, fontSize=15)
        (x, y) = nextAvailable[3]
        nextAvailable = display.add_string(x, y, 128, 64, currentHumidity, fontSize=10)
        display.display_everything()

        time.sleep(0.5)

def weather_monitor():
    pass

def datetime_monitor():
    pass


if (__name__ == "__main__"):
    main()