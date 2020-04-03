#! /usr/bin/python3
import subprocess
import time
import datetime

import weatherHandler
import timeHandler
import displayHandler

import RPi.GPIO as GPIO

def main():
    WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    DATE_FORMAT = '%Y-%m-%d %a \n%H:%M:%S \n'
    
    weather = weatherHandler.cityWeather(refreshInterval=3, cityID="5083221"); 
    display = displayHandler.SerialOLEDDisplay(128, 64)

    for i in range(10):
        dt = datetime.datetime.now()
        currentWeather     = weather.get_current_weather()
        currentTemperature = weather.get_current_temperature()
        currentHumidity    = weather.get_current_humidity()
        display.display_string(0, 0, currentWeather, fontSize=20)
 
if (__name__ == "__main__"):
    main()