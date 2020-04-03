import json
import datetime

from urllib.request import *
from urllib.error   import *

class cityWeather() : 

    def __init__(self, refreshInterval=60, \
                 cityID="", city="", country="", tempUnit="C"): 
        self.API_URL = "https://api.openweathermap.org/data/2.5/"
        self.APP_ID  = "f191b428a66f81a31f3d3ef4bd50e7c4"\

        self.cityID   = cityID
        self.city     = city
        self.country  = country
        self.tempUnit = tempUnit

        self.currentTime = datetime.datetime.now()
        self.refreshInterval = refreshInterval
        self.refreshTime = self.currentTime + datetime.timedelta(seconds=self.refreshInterval)

        self.refresh_weather()

    #Checks the current weather of the given city with the openweathermap
    #   api. 
    #Returns the weather of the given city in a formatted way. 
    #city: the city to be checked. 
    #tempUnit: the desired unit for temperature. 
    #Currently only works with city id. 
    def refresh_weather(self):
        weatherJson = self.query("weather", self.cityID)

        self.weather = weatherJson["weather"][0]["main"]
        self.temp    = self.conv_temp(weatherJson["main"]["temp"])
        self.humidity= weatherJson["main"]["humidity"]
    #Three getters for respective variables. 
    def get_current_weather(self):
        self.check_refresh()
        return self.weather
    
    def get_current_temperature(self):
        self.check_refresh()
        return self.temp
    
    def get_current_humidity(self):
        self.check_refresh()
        return self.humidity


    #Acquires a five-day forecast of the given city with the openweathermap
    #   api. 
    #Returns the forecast for the given city in a formatted way. 
    #city: the city to be checked. 
    #tempUnit: the desired unit for temperature.
    #Currently only works with city id. 
    def forecast(self): 
        weatherJson = self.query("forecast", self.cityID)

    #Looks up the given city in the OpenWeatherMap city list and returns 
    #   the id of that city. 
    #TODO: implement binary search. 
    def city_lookup(city=""):
        cityIDList = open("cityIDs", "r")

    #Sends the request to the API and returns a processed json of the 
    #   returned information. 
    def query(self, queryType, cityID="", city="", country=""):
        url = self.API_URL + queryType + "?id=" + cityID + "&appid=" + self.APP_ID
        
        response    = urlopen(url)
        contentStr  = response.read().decode('utf-8')
        contentJson = json.loads(contentStr)

        return contentJson
    
    #Converts temperature from one unit to another. 
    #temp: temperature taken in. Assumed to be Kelvin. 
    #unit: unit to be converted to. 
    def conv_temp(self, temp, unit="C"):
        if (unit == "C"):
            return temp - 273.15
        elif (unit == "F"):
            return (temp - 273.15) * (9/5) + 32
        else: 
            return temp
    
    #Checks to see if it is time to refresh the weather 
    #information, and refreshes the information when needed. 
    def check_refresh(self):
        self.currentTime = datetime.datetime.now()
        if (self.refreshTime < self.currentTime):
            self.refresh_weather()
        else: 
            return