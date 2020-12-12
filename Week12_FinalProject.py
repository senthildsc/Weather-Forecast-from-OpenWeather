'''
File              : Week12_FinalProject.py
Name              : Senthilraj Srirangan
Date              : 06/01/2019
Assignment Number : 12.1
Course            : DSC 510 - Introduction to Programming
Description       : Program to request weather forecast data from OpenWeatherMap API
'''

import sys
import json
import requests
from datetime import datetime

global uom

def establish_APIConnection(input_city):
    global uom
    CITY = input_city
    API_KEY = 'ad5875aa934dd46d61de4dd4ea3d28a1'
    try:
        units = input('imperial or metric?')                                            # Selecting the Unit of Measure
        if units == 'imperial':
            uom = 'F'
        elif units == 'metric':
            uom = 'C'
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units={}&APPID={}".format(CITY,units,API_KEY)    # API Call
        headers = {'cache-control': 'no-cache'}
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        data = json.loads(response.text)
        Response_Code = data['cod']
        if str(Response_Code) == '200':
            print('Congratulations . Your Connection was successful\n')
            return data
        else:
            print('Your Connection was not successful')
    except requests.exceptions.HTTPError as e:
        Response_Code = str(e)
        if Response_Code[0:3] == '401':
            print('Invalid API key. Please see http://openweathermap.org/faq  #error401 for more info.')
        elif Response_Code[0:3] == '429':
            print('API Key Blocked . Please see http://openweathermap.org/faq #error429 for more info.')
        elif Response_Code[0:3] == '404':
            print('Wrong API request ,City not found. Please see http://openweathermap.org/faq #error404 for more info.')
        else:
            print(str(e))
        sys.exit(1)

def convert_time(time):
    converted_time = datetime.fromtimestamp(time).strftime('%I:%M %p')          # convert to Time
    return converted_time

def print_output(weather_data):                                                 # Print the Output
    global uom
    print('Current weather Status in: {}, {}'.format(weather_data["CityName"],weather_data["Country"]))
    print('---------------------------------------------------------------')
    print('Temperature Status')
    print('Current Temperature : {} {}, and the Cloud is : {}'.format(weather_data["Temp"],uom, weather_data["Cloudiness"]))
    print('MaxTemp: {} {} , MinTemp: {} {}'.format(weather_data["Max_Temp"],uom,weather_data["Min_Temp"],uom))
    print('Humidity  : {}'.format(weather_data["Humidity"]))
    print('WindSpeed : {} m/h'.format(weather_data["Wind_Speed"]))
    print('Sunrise   : {}'.format(weather_data["Sunrise"]))
    print('Sunset    : {}'.format(weather_data["Sunset"]))
    print('Latitude  : {}'.format(weather_data["Latitude"]))
    print('Longitude : {}'.format(weather_data["Longitude"]))


def Extract_WeatherInfo(data):                                      # Storing in dictionary
        weather_data = dict(
            CityName=data['name'],
            TimeZone=data['timezone'],
            Date=convert_time(data['dt']),
            Longitude=data['coord']['lon'],
            Latitude=data['coord']['lat'],
            Cloudiness= data['weather'][0]['description'],
            Temp=data['main']['temp'],
            Humidity=data['main']['humidity'],
            Min_Temp=data['main']['temp_min'],
            Max_Temp=data['main']['temp_max'],
            Wind_Speed=data['wind']['speed'],
            Country=data['sys']['country'],
            Sunrise=convert_time(data['sys']['sunrise']),
            Sunset=convert_time(data['sys']['sunset'])
        )
        return weather_data

def main():
    print('Welcome to OpenWeather Map Forecast ')
    while True:
            user_input = str(input('Please enter the ZipCode or CityName to get Weather status or No to Quit: '))  # User Input
            input_str = user_input.strip(' ')                                   # strip leading spaces
            input_city = input_str.replace(" ", "")
            if input_city.isalnum() is True and input_city.upper() != 'NO':
                data = establish_APIConnection(input_city)                      # Establish API Connection and Extract Data
                weather_data = Extract_WeatherInfo(data)                        # Parse the Data and store in Dictionary
                print_output(weather_data)                                      # Print the Output
            elif input_city.upper()== 'NO':
                print('Thank you . Please visit later if you would like to know Weather Details')
                break
            else:
                print('Please enter valid Input')

if __name__ == "__main__":
    main()

