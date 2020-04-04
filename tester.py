#! /usr/bin/python3
import subprocess
import time
import datetime

import weatherHandler
import displayHandler

import RPi.GPIO as GPIO

display = displayHandler.SerialOLEDDisplay(128, 64)
display.add_string(0, 0, maxX=32, maxY=32, string="Good day fellers this is a line", fontSize=10)
display.display_everything()