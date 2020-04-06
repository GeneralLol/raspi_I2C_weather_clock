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

    weather = weatherHandler.cityWeather(refreshInterval=10, cityID="5083221"); 
    display = displayHandler.SerialOLEDDisplay(128, 64)

    refreshtime = 1

    while (True):
        #cycleStart is used to calculate the execution time of one cycle
        #   and adjust the sleep time. 
        cycleStart = time.clock_gettime(time.CLOCK_MONOTONIC)

        currentDatetime    = datetime.datetime.now()
        currentDateStr = currentDatetime.date().strftime(DATE_FORMAT)
        currentTimeStr = currentDatetime.time().strftime(TIME_FORMAT)
        currentWeather     = weather.get_current_weather()
        currentTemperature = weather.get_current_temperature()
        currentHumidity    = weather.get_current_humidity()

        #Print everything out for debug purposes
        debug_str = "{}\n{}\n{}\n{}\n{}\n{}\n".format(\
                                            cycleStart,\
                                            currentDateStr, \
                                            currentTimeStr, \
                                            currentWeather, \
                                            currentTemperature, \
                                            currentHumidity)
        print("acquired values:")
        print(debug_str)

        #If the time is between 7pm and 8am, dim the display. 
        if (currentDatetime.time() < datetime.time(hour=8) or \
            currentDatetime.time() > datetime.time(hour=19)):
            display.config_brightness(0)
        else:
            display.config_brightness(255)

        draw_on_display(display, currentDateStr, currentTimeStr, \
                        currentWeather, currentTemperature, currentHumidity)

        cycleEnd = time.clock_gettime(time.CLOCK_MONOTONIC)
        cycleDelta = cycleEnd - cycleStart

        sleepTime = refreshTime - cycleDelta
        if (sleepTime < 0):
            sleepTime = 0.000000001
        time.sleep(sleepTime)

def weather_monitor():
    pass

def datetime_monitor():
    pass

def draw_on_display(display, dateStr, timeStr, weatherStr, tempStr, humidityStr):
    #Draw things onto the display (basically hard-coding)
    display.clear_buffer()
    (x, y) = (0, 0)
    nextAvailable = display.add_string(x, y, 128, 13, dateStr, fontSize=13)
    (x, y) = nextAvailable[3]
    nextAvailable = display.add_string(x, y, 128, 30, timeStr, fontSize=17)
    (x, y) = nextAvailable[3]
    nextAvailable = display.add_string(x, y, 90, 64, weatherStr, fontSize=25)
    (x, y) = nextAvailable[1]
    x = 90
    nextAvailable = display.add_string(x, y, 128, 47, tempStr, fontSize=15)
    (x, y) = nextAvailable[3]
    nextAvailable = display.add_string(x, y, 128, 64, humidityStr, fontSize=10)
    display.display_everything()

if (__name__ == "__main__"):
    main()